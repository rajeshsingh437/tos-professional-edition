"""
SENTRY — Flattrade Relay Server
Runs on the Oracle Cloud VM (the one with the registered static IP), NOT on
your home PC. This is the only piece of SENTRY that talks to Flattrade
directly — everything else (dashboard, journal, tags, local database) stays
on your PC exactly as before.

Why this exists: Flattrade/SEBI require API token generation and every
order/account call to originate from your registered static IP. Your home
PC's IP isn't that — this VM's IP is. So the token and every Flattrade call
live here; your PC only talks to this relay over a private shared secret.

Endpoints:
    GET  /health                 - confirms the relay is running
    POST /complete_login         - body: {"code": "..."} — finishes the
                                    OAuth flow using the code your PC caught
                                    from the browser redirect
    GET  /login_status           - whether a valid Flattrade session exists
    GET  /positions               \
    GET  /orders                   |  read-only account data, matching
    GET  /trades                   |  SENTRY's observe-only philosophy —
    GET  /limits                   |  no order placement here on purpose
    GET  /holdings                /

Every endpoint except /health requires:
    Authorization: Bearer <RELAY_SHARED_SECRET>
so nothing but your own SENTRY app can use this relay.
"""

import hashlib
import json
import os
import time

import requests
from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# Config — loaded from a local .env file (NEVER commit this — see .gitignore
# in this folder). Copy .env.example to .env and fill in your real values.
# ---------------------------------------------------------------------------
def load_env(path=".env"):
    values = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                values[key.strip()] = value.strip().strip("'").strip('"')
    return values


ENV = load_env()
BROKER_API_KEY = ENV.get("BROKER_API_KEY", "")
BROKER_API_SECRET = ENV.get("BROKER_API_SECRET", "")
RELAY_SHARED_SECRET = ENV.get("RELAY_SHARED_SECRET", "")

LOGIN_URL = "https://auth.flattrade.in/"
TOKEN_URL = "https://authapi.flattrade.in/trade/apitoken"
API_BASE_URL = "https://piconnect.flattrade.in/PiConnectAPI"
REQUEST_TIMEOUT = 15

app = Flask(__name__)

# In-memory session — lost on restart by design (simple, and forces a fresh
# login each time the relay restarts, which is the safer default for a
# personal-use VM). If you want it to survive restarts, this could be
# written to a local file instead — flag it if you want that changed.
session = {"access_token": "", "client_id": ""}


def require_auth():
    """Returns True if the request carries the correct shared secret."""
    auth = request.headers.get("Authorization", "")
    return auth == f"Bearer {RELAY_SHARED_SECRET}" and bool(RELAY_SHARED_SECRET)


def flattrade_post(endpoint, payload):
    """Authenticated POST to a Flattrade REST endpoint, from this VM's IP."""
    if not session["access_token"] or not session["client_id"]:
        raise RuntimeError("Not logged in — call /complete_login first")

    response = requests.post(
        f"{API_BASE_URL}/{endpoint}",
        data={
            "jData": json.dumps(payload),
            "jKey": session["access_token"],
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    result = response.json()
    if isinstance(result, dict) and result.get("stat") == "Not_Ok":
        raise RuntimeError(result.get("emsg") or f"{endpoint} failed")
    return result


def account_payload(**extra):
    return {"uid": session["client_id"], "actid": session["client_id"], **extra}


@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": time.time()})


@app.route("/complete_login", methods=["POST"])
def complete_login():
    if not require_auth():
        return jsonify({"error": "unauthorized"}), 401

    code = (request.json or {}).get("code")
    if not code:
        return jsonify({"error": "missing 'code'"}), 400

    # Flattrade's required security-key hash: sha256(api_key + code + api_secret)
    security_key = hashlib.sha256(
        f"{BROKER_API_KEY}{code}{BROKER_API_SECRET}".encode("utf-8")
    ).hexdigest()

    try:
        resp = requests.post(
            TOKEN_URL,
            json={
                "api_key": BROKER_API_KEY,
                "request_code": code,
                "api_secret": security_key,
            },
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        payload = resp.json()
    except Exception as e:
        return jsonify({"error": f"token exchange failed: {e}"}), 502

    if payload.get("status") != "Ok" or not payload.get("token"):
        return jsonify({"error": payload.get("emsg") or "login failed"}), 400

    session["access_token"] = str(payload["token"])
    session["client_id"] = str(payload.get("client", ""))
    return jsonify({"status": "logged in", "client_id": session["client_id"]})


@app.route("/login_status")
def login_status():
    if not require_auth():
        return jsonify({"error": "unauthorized"}), 401
    return jsonify({"authenticated": bool(session["access_token"])})


def make_readonly_route(name, endpoint, extra_payload=None):
    def handler():
        if not require_auth():
            return jsonify({"error": "unauthorized"}), 401
        try:
            result = flattrade_post(endpoint, account_payload(**(extra_payload or {})))
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 502
    handler.__name__ = name
    return handler


app.add_url_rule("/positions", "positions", make_readonly_route("positions", "PositionBook"))
app.add_url_rule("/orders", "orders", make_readonly_route("orders", "OrderBook"))
app.add_url_rule("/trades", "trades", make_readonly_route("trades", "TradeBook"))
app.add_url_rule("/limits", "limits", make_readonly_route("limits", "Limits"))
app.add_url_rule("/holdings", "holdings", make_readonly_route("holdings", "Holdings", {"prd": "C"}))


if __name__ == "__main__":
    if not BROKER_API_KEY or not BROKER_API_SECRET:
        print("WARNING: BROKER_API_KEY / BROKER_API_SECRET not set — copy .env.example to .env and fill them in.")
    if not RELAY_SHARED_SECRET:
        print("WARNING: RELAY_SHARED_SECRET not set — anyone who finds this server could use it. Set one in .env.")
    app.run(host="0.0.0.0", port=8090)

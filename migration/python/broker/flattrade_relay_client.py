"""
SENTRY — flattrade_relay_client.py
Runs on your home PC, as part of SENTRY itself. This is the "local half" of
the relay architecture (see oracle_relay/relay_server.py for the "remote
half" that runs on your Oracle VM).

Split of responsibility:
  - THIS file: opens your browser to Flattrade's login page, runs a brief
    local server to catch the redirect (must be local — the registered
    redirect URL is 127.0.0.1, which only means anything relative to
    wherever your browser is), then hands the resulting code to the relay.
  - The relay (on the VM): does the actual token exchange and every
    subsequent Flattrade API call, from the registered static IP.

Nothing in this file talks to Flattrade directly except the one-time
authorization-URL redirect — everything else goes through the relay.
"""

import threading
import time
import webbrowser

import requests
from flask import Flask, request

LOGIN_URL = "https://auth.flattrade.in/"
LOCAL_CALLBACK_HOST = "127.0.0.1"
LOCAL_CALLBACK_PORT = 5000
LOCAL_CALLBACK_PATH = "/flattrade/callback"
OAUTH_WAIT_TIMEOUT_SECONDS = 180
REQUEST_TIMEOUT = 15


class _CallbackCatcher:
    """A short-lived local Flask server that exists only to catch the
    Flattrade redirect and grab the 'code' query parameter."""

    def __init__(self):
        self.code = None
        self.app = Flask(__name__)

        @self.app.route(LOCAL_CALLBACK_PATH)
        def callback():
            self.code = request.args.get("code") or request.args.get("request_code")
            if not self.code:
                return "<h3>Login callback did not include a code.</h3>", 400
            return (
                "<html><body style='font-family:sans-serif; text-align:center; margin-top:80px;'>"
                "<h2>SENTRY</h2><h3>Login received — you can close this window.</h3>"
                "</body></html>"
            )

    def start(self):
        thread = threading.Thread(
            target=self.app.run,
            kwargs={"host": LOCAL_CALLBACK_HOST, "port": LOCAL_CALLBACK_PORT, "debug": False, "use_reloader": False},
            daemon=True,
        )
        thread.start()

    def wait_for_code(self, timeout=OAUTH_WAIT_TIMEOUT_SECONDS):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.code:
                return self.code
            time.sleep(0.25)
        raise TimeoutError("Timed out waiting for the Flattrade login redirect.")


def _relay_headers(relay_secret):
    return {"Authorization": f"Bearer {relay_secret}"}


def login(api_key, relay_url, relay_secret):
    """
    Opens your browser for the Flattrade login, catches the redirect
    locally, then hands the code to the relay to finish the process.
    Returns the relay's response (e.g. {"status": "logged in", "client_id": "..."}).
    """
    if not api_key or not relay_url or not relay_secret:
        raise ValueError("api_key, relay_url, and relay_secret are all required")

    catcher = _CallbackCatcher()
    catcher.start()

    authorization_url = f"{LOGIN_URL}?app_key={api_key}"
    webbrowser.open(authorization_url)

    code = catcher.wait_for_code()

    resp = requests.post(
        f"{relay_url.rstrip('/')}/complete_login",
        json={"code": code},
        headers=_relay_headers(relay_secret),
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def login_status(relay_url, relay_secret):
    resp = requests.get(
        f"{relay_url.rstrip('/')}/login_status",
        headers=_relay_headers(relay_secret),
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def _get(endpoint, relay_url, relay_secret):
    resp = requests.get(
        f"{relay_url.rstrip('/')}/{endpoint}",
        headers=_relay_headers(relay_secret),
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def get_positions(relay_url, relay_secret):
    return _get("positions", relay_url, relay_secret)


def get_orders(relay_url, relay_secret):
    return _get("orders", relay_url, relay_secret)


def get_trades(relay_url, relay_secret):
    return _get("trades", relay_url, relay_secret)


def get_limits(relay_url, relay_secret):
    return _get("limits", relay_url, relay_secret)


def get_holdings(relay_url, relay_secret):
    return _get("holdings", relay_url, relay_secret)

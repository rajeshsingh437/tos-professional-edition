"""
AEGIS

OAuth Callback Server

Receives the OAuth callback from Flattrade and forwards the
request_code to the Oracle Relay Server.

The local PC NEVER exchanges tokens directly with Flattrade.
"""

from __future__ import annotations

import threading
import requests

from flask import Flask, request

from src.core.broker.constants import (
    CALLBACK_HOST,
    CALLBACK_PORT,
)

from config.settings import load_broker


class OAuthServer:
    """
    Local OAuth callback server.
    """

    def __init__(self) -> None:

        self.request_code: str | None = None
        self.ready = False

        broker = load_broker()

        self.relay_url = broker["relay_url"]
        self.relay_secret = broker["relay_shared_secret"]

        self.app = Flask(__name__)

        self._configure_routes()

    # ==========================================================
    # Routes
    # ==========================================================

    def _configure_routes(self) -> None:

        @self.app.route("/flattrade/callback")
        def callback():

            print("\n" + "=" * 70)
            print("CALLBACK ROUTE ENTERED")
            print("URL :", request.url)
            print("ARGS:", dict(request.args))
            print("=" * 70)

            self.request_code = (
                request.args.get("code")
                or request.args.get("request_code")
            )

            print("Extracted request_code:", self.request_code)
            print()

            try:

                url = f"{self.relay_url}/complete_login"

                print("Sending request code to Oracle Relay")
                print(url)
                print()

                response = requests.post(
                    url,
                    json={
                        "code": self.request_code,
                    },
                    headers={
                        "Authorization":
                        f"Bearer {self.relay_secret}"
                    },
                    timeout=30,
                )

                print("Relay HTTP Status :", response.status_code)

                payload = response.json()

                print("Relay Response")
                print(payload)
                print("=" * 70)
                print()

                if response.status_code != 200:

                    return (
                        "<html>"
                        "<body style='font-family:Arial;"
                        "text-align:center;"
                        "margin-top:80px;'>"
                        "<h2>AEGIS</h2>"
                        "<h3>Login Failed</h3>"
                        f"<p>{payload.get('error')}</p>"
                        "</body>"
                        "</html>",
                        500,
                    )

            except Exception as e:

                import traceback

                traceback.print_exc()

                return (
                    "<html>"
                    "<body style='font-family:Arial;"
                    "text-align:center;"
                    "margin-top:80px;'>"
                    "<h2>AEGIS</h2>"
                    "<h3>Unable to contact Oracle Relay</h3>"
                    f"<p>{e}</p>"
                    "</body>"
                    "</html>",
                    500,
                )

            self.stop_server()

            return (
                "<html>"
                "<body style='font-family:Arial;"
                "text-align:center;"
                "margin-top:80px;'>"
                "<h2>AEGIS</h2>"
                "<h3>Login Successful</h3>"
                "<p>Oracle Relay authenticated successfully.</p>"
                "<p>You may close this window.</p>"
                "</body>"
                "</html>"
            )

    # ==========================================================
    # Server
    # ==========================================================

    def start(self) -> None:

        def run_server():

            try:

                print(
                    f"OAuth callback server listening on "
                    f"http://{CALLBACK_HOST}:{CALLBACK_PORT}/flattrade/callback"
                )

                self.ready = True

                self.app.run(
                    host=CALLBACK_HOST,
                    port=CALLBACK_PORT,
                    debug=False,
                    use_reloader=False,
                )

            except Exception:

                import traceback

                print()
                print("=" * 70)
                print("CALLBACK SERVER FAILED")
                print("=" * 70)

                traceback.print_exc()

                print("=" * 70)

        self._thread = threading.Thread(
            target=run_server,
            daemon=True,
        )

        self._thread.start()

    def stop_server(self) -> None:

        func = request.environ.get(
            "werkzeug.server.shutdown"
        )

        if func is not None:

            try:
                func()
            except Exception:
                pass

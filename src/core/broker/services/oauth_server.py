"""
AEGIS

OAuth Callback Server

Receives the OAuth callback from Flattrade.

Its ONLY responsibility is to receive the request code and
make it available to the broker adapter.

The broker adapter is responsible for calling the Oracle Relay.
"""

from __future__ import annotations

import threading

from flask import Flask, request

from src.core.broker.constants import (
    CALLBACK_HOST,
    CALLBACK_PORT,
)


class OAuthServer:
    """
    Local OAuth callback server.
    """

    def __init__(self) -> None:

        self.request_code: str | None = None
        self.ready = False

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

            self.stop_server()

            return (
                "<html>"
                "<body style='font-family:Arial;"
                "text-align:center;"
                "margin-top:80px;'>"
                "<h2>AEGIS</h2>"
                "<h3>Login Successful</h3>"
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

"""
AEGIS

Flattrade OAuth Callback Server
"""

from __future__ import annotations

import threading

from flask import Flask
from flask import request

from brokers.flattrade.constants import (
    CALLBACK_HOST,
    CALLBACK_PORT,
)


class OAuthServer:
    """
    Small local HTTP server used to receive
    the OAuth callback from Flattrade.
    """

    def __init__(self) -> None:

        self.request_code: str | None = None

        self.app = Flask(__name__)

        self._configure_routes()

    def _configure_routes(self) -> None:

        @self.app.route("/callback")
        def callback():

            self.request_code = request.args.get(
                "request_code"
            )

            return """
            <html>
                <body style="font-family:Arial;
                             text-align:center;
                             margin-top:80px;">
                    <h2>AEGIS</h2>

                    <h3>
                        Login Successful
                    </h3>

                    <p>
                        You may now close this window.
                    </p>

                </body>
            </html>
            """

    def start(self) -> None:
        """
        Start local callback server.
        """

        thread = threading.Thread(
            target=self.app.run,
            kwargs={
                "host": CALLBACK_HOST,
                "port": CALLBACK_PORT,
                "debug": False,
                "use_reloader": False,
            },
            daemon=True,
        )

        thread.start()

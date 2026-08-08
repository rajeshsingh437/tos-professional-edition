"""
AEGIS

OAuth Callback Server

Receives the OAuth callback from Flattrade
and captures the request_code.
"""

from __future__ import annotations

import logging
import threading

from flask import Flask, request

from brokers.flattrade.constants import (
    CALLBACK_HOST,
    CALLBACK_PORT,
)

logger = logging.getLogger(__name__)


class OAuthServer:
    """
    Local callback server.
    """

    def __init__(self) -> None:

        self.request_code: str | None = None

        self.app = Flask(__name__)

        self._configure_routes()

    # ==========================================================
    # Routes
    # ==========================================================

    def _configure_routes(self) -> None:

        @self.app.route("/flattrade/callback")
        def callback():
            logger.info("OAuth callback request received.")

            self.request_code = (
                request.args.get("code")
                or request.args.get("request_code")
            )

            if not self.request_code:
                logger.error("No authorization code received in callback.")
                return (
                    "<h2>AEGIS</h2>"
                    "<h3>No authorization code received.</h3>",
                    400,
                )

            logger.info("Authorization code captured successfully.")

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
        logger.info(
            "Starting OAuth callback server on %s:%s",
            CALLBACK_HOST,
            CALLBACK_PORT,
        )

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

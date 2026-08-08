"""
AEGIS
Flattrade OAuth Service
Standalone OAuth callback server.

Responsibilities
----------------
1. Start local HTTP callback server
2. Receive request_code
3. Exchange request_code for access token
4. Save authenticated session
5. Shutdown automatically
"""

from __future__ import annotations

import threading
import time
import webbrowser
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
)
from typing import Any
from urllib.parse import (
    parse_qs,
    urlparse,
)

from ..constants import (
    CALLBACK_HOST,
    CALLBACK_PORT,
)
from .auth_manager import (
    AuthenticationManager,
)
from .oauth_client import (
    OAuthClient,
)


class OAuthService:
    """
    Handles complete OAuth authentication.
    """

    auth: AuthenticationManager
    oauth: OAuthClient
    request_code: str | None
    server: HTTPServer | None
    server_thread: threading.Thread | None

    def __init__(self) -> None:
        self.auth = AuthenticationManager()
        self.oauth = OAuthClient(
            api_key=self.auth.broker["api_key"],
            api_secret=self.auth.broker["api_secret"],
        )
        self.request_code = None
        self.server = None
        self.server_thread = None

    def start_server(self) -> None:
        """
        Start local callback server.
        """
        OAuthRequestHandler.service = self
        self.server = HTTPServer(
            (
                CALLBACK_HOST,
                CALLBACK_PORT,
            ),
            OAuthRequestHandler,
        )
        print(
            f"OAuth callback server started at "
            f"http://{CALLBACK_HOST}:{CALLBACK_PORT}/flattrade/callback"
        )
        self.server.serve_forever()

    def launch_server(self) -> None:
        """
        Launch callback server in background.
        """
        self.server_thread = threading.Thread(
            target=self.start_server,
            daemon=True,
        )
        self.server_thread.start()
        time.sleep(0.5)

    def stop_server(self) -> None:
        """
        Stop callback server.
        """
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None

    def authenticate(self) -> bool:
        """
        Complete Flattrade OAuth authentication.
        """
        # Existing session
        if self.auth.is_authenticated:
            print("Existing authenticated session found.")
            return True

        # Start callback server
        self.launch_server()

        # Open browser
        print("Opening Flattrade login...")
        webbrowser.open(self.oauth.authorization_url)

        print("Waiting for OAuth callback...")
        while self.request_code is None:
            time.sleep(0.25)

        print("Authorization code received.")
        payload: dict[str, Any] = self.oauth.exchange_request_code(self.request_code)

        access_token: str = payload["token"]
        self.auth.save_authenticated_session(
            access_token=access_token,
            client_id=self.auth.broker["api_key"],
        )

        self.stop_server()
        print("Authentication successful.")
        return True


class OAuthRequestHandler(BaseHTTPRequestHandler):
    """
    Handles Flattrade OAuth callback.
    """

    service: OAuthService

    def do_GET(self) -> None:
        """
        Handle GET requests for the OAuth callback.
        """
        parsed = urlparse(self.path)
        if parsed.path != "/flattrade/callback":
            self.send_response(404)
            self.end_headers()
            return

        query = parse_qs(parsed.query)
        request_code: str | None = None

        if "request_code" in query:
            request_code = query["request_code"][0]
        elif "code" in query:
            request_code = query["code"][0]

        if request_code is None:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No request_code received.")
            return

        self.service.request_code = request_code

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html",
        )
        self.end_headers()
        self.wfile.write(
            b"""
            <html>
            <body
            style="
            font-family:Arial;
            text-align:center;
            margin-top:100px;
            "
            >
            <h2>AEGIS</h2>
            <h3>
            Login Successful
            </h3>
            <p>
            You may close this window.
            </p>
            </body>
            </html>
            """
        )

    def log_message(self, format: str, *args: Any) -> None:
        """
        Disable HTTP logging.
        """
        return

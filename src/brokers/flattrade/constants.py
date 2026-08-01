"""
AEGIS

Flattrade Constants
"""

from __future__ import annotations

# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------

AUTH_BASE_URL = "https://authapi.flattrade.in"

LOGIN_URL = f"{AUTH_BASE_URL}/trade/login"

TOKEN_URL = f"{AUTH_BASE_URL}/trade/apitoken"


# ------------------------------------------------------------------
# API
# ------------------------------------------------------------------

API_BASE_URL = "https://piconnect.flattrade.in/PiConnectTP"


# ------------------------------------------------------------------
# WebSocket
# ------------------------------------------------------------------

WEBSOCKET_URL = "wss://piconnect.flattrade.in/PiConnectWSTp/"


# ------------------------------------------------------------------
# Local OAuth Callback
# ------------------------------------------------------------------

CALLBACK_HOST = "127.0.0.1"

CALLBACK_PORT = 8765

CALLBACK_URL = (
    f"http://{CALLBACK_HOST}:{CALLBACK_PORT}/callback"
)


# ------------------------------------------------------------------
# Session
# ------------------------------------------------------------------

SESSION_FILENAME = "session.json"


# ------------------------------------------------------------------
# Timeouts
# ------------------------------------------------------------------

REQUEST_TIMEOUT = 15

HEARTBEAT_SECONDS = 20

RECONNECT_DELAY = 5

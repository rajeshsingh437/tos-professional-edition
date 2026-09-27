"""
AEGIS

Broker Constants

Shared Flattrade configuration used by all broker services.
"""

from __future__ import annotations

# ==========================================================
# Authentication
# ==========================================================

LOGIN_URL = "https://auth.flattrade.in/"

TOKEN_URL = "https://authapi.flattrade.in/trade/apitoken"

# ==========================================================
# REST API
# ==========================================================

API_BASE_URL = "https://piconnect.flattrade.in/PiConnectAPI"

# ==========================================================
# WebSocket
# ==========================================================

WEBSOCKET_URL = "wss://piconnect.flattrade.in/PiConnectWSAPI/"

# ==========================================================
# Local OAuth Callback
# ==========================================================

CALLBACK_HOST = "127.0.0.1"

CALLBACK_PORT = 5000

CALLBACK_PATH = "/flattrade/callback"

CALLBACK_URL = (
    f"http://{CALLBACK_HOST}:{CALLBACK_PORT}{CALLBACK_PATH}"
)

# ==========================================================
# Session
# ==========================================================

SESSION_FILENAME = "session.json"

# ==========================================================
# Network
# ==========================================================

REQUEST_TIMEOUT = 15

HEARTBEAT_SECONDS = 20

RECONNECT_DELAY = 5

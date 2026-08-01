"""
AEGIS

Broker Manager
"""

from __future__ import annotations

from brokers.flattrade.auth_manager import AuthenticationManager
from brokers.flattrade.oauth_server import OAuthServer
from brokers.flattrade.oauth_client import OAuthClient
from brokers.flattrade.rest import RestClient
from brokers.flattrade.websocket import WebSocketClient


class BrokerManager:
    """
    Coordinates all broker services.
    """

    def __init__(self):

        self.auth = AuthenticationManager()

        self.oauth_server = OAuthServer()

        self.oauth = OAuthClient(
            self.auth.broker["api_key"],
            self.auth.broker["api_secret"],
        )

        self.rest = None

        self.websocket = None

    @property
    def connected(self):

        return (
            self.websocket is not None
            and self.websocket.connected
        )

    def start(self):

        self.oauth_server.start()

    def create_clients(
        self,
        access_token: str,
    ):

        self.rest = RestClient(access_token)

        self.websocket = WebSocketClient(
            access_token
        )

    def connect(self):

        if self.websocket:

            self.websocket.connect()

    def disconnect(self):

        if self.websocket:

            self.websocket.disconnect()

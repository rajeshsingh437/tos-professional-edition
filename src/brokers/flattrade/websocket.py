"""
AEGIS

Flattrade WebSocket Client
"""

from __future__ import annotations

import threading

from websocket import WebSocketApp

from brokers.flattrade.constants import (
    HEARTBEAT_SECONDS,
    WEBSOCKET_URL,
)


class WebSocketClient:
    """
    Handles Flattrade realtime market feed.
    """

    def __init__(self, access_token: str):

        self.access_token = access_token

        self.ws: WebSocketApp | None = None

        self.connected = False

    def connect(self):

        self.ws = WebSocketApp(
            WEBSOCKET_URL,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )

        threading.Thread(
            target=self.ws.run_forever,
            daemon=True,
        ).start()

    def disconnect(self):

        if self.ws:

            self.ws.close()

    def subscribe(self, symbols: list[str]):

        raise NotImplementedError

    def unsubscribe(self, symbols: list[str]):

        raise NotImplementedError

    def heartbeat(self):

        raise NotImplementedError

    def _on_open(self, ws):

        self.connected = True

        print("Broker websocket connected.")

    def _on_close(
        self,
        ws,
        close_status_code,
        close_msg,
    ):

        self.connected = False

        print("Broker websocket disconnected.")

    def _on_error(
        self,
        ws,
        error,
    ):

        print(error)

    def _on_message(
        self,
        ws,
        message,
    ):

        print(message)

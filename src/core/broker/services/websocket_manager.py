"""
AEGIS

Broker WebSocket Manager
"""

from __future__ import annotations

import threading

from websocket import WebSocketApp

from src.core.broker.constants import (
    HEARTBEAT_SECONDS,
    WEBSOCKET_URL,
)


class WebSocketManager:
    """
    Handles broker realtime websocket connection.
    """

    def __init__(
        self,
        access_token: str,
    ) -> None:

        self.access_token = access_token

        self.ws: WebSocketApp | None = None

        self.connected = False

    def connect(self) -> None:

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

    def disconnect(self) -> None:

        if self.ws:

            self.ws.close()

    def subscribe(
        self,
        symbols: list[str],
    ) -> None:

        raise NotImplementedError

    def unsubscribe(
        self,
        symbols: list[str],
    ) -> None:

        raise NotImplementedError

    def heartbeat(self) -> None:

        raise NotImplementedError

    def _on_open(
        self,
        ws,
    ) -> None:

        self.connected = True

        print("Broker websocket connected.")

    def _on_close(
        self,
        ws,
        close_status_code,
        close_msg,
    ) -> None:

        self.connected = False

        print("Broker websocket disconnected.")

    def _on_error(
        self,
        ws,
        error,
    ) -> None:

        print(error)

    def _on_message(
        self,
        ws,
        message,
    ) -> None:

        print(message)

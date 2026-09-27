"""
AEGIS

Flattrade WebSocket Manager

Handles Flattrade PiConnect API V2 realtime WebSocket communication.

Responsibilities
----------------
- WebSocket connection lifecycle
- Flattrade V2 authentication
- Automatic reconnect
- Touchline subscriptions
- Touchline unsubscriptions
- Heartbeat
- Incoming message parsing
- Tick callback dispatch
- Subscription persistence across reconnects
- Thread-safe WebSocket writes
"""

from __future__ import annotations

import json
import logging
import threading
import time
from typing import Any, Callable

from websocket import WebSocketApp

from src.core.broker.constants import (
    HEARTBEAT_SECONDS,
    RECONNECT_DELAY,
    WEBSOCKET_URL,
)


logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages the Flattrade PiConnect API V2 WebSocket.

    The manager deliberately keeps broker-specific WebSocket
    protocol handling inside this service so that the rest of
    AEGIS can consume normalized realtime events through callbacks.
    """

    def __init__(
        self,
        access_token: str,
        client_id: str,
        on_tick: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:

        if not access_token:
            raise ValueError(
                "access_token is required."
            )

        if not client_id:
            raise ValueError(
                "client_id is required."
            )

        self.access_token = access_token
        self.client_id = client_id

        self.ws: WebSocketApp | None = None

        self.connected = False
        self.authenticated = False
        self.running = False

        self.on_tick = on_tick

        self.lock = threading.RLock()

        self.last_tick = 0.0
        self.last_heartbeat = 0.0

        # Symbols currently requested by AEGIS.
        #
        # Format:
        #
        #     NSE|2885
        #     NFO|35008
        #
        self.subscriptions: set[str] = set()

        self.reconnect_delay = RECONNECT_DELAY

        self.receiver_thread: threading.Thread | None = None

        self.heartbeat_thread: threading.Thread | None = None

        self._stop_event = threading.Event()

    # ==========================================================
    # Connection Lifecycle
    # ==========================================================

    def connect(self) -> None:
        """
        Start the WebSocket connection in a background thread.

        Calling connect() more than once is safe.
        """

        with self.lock:

            if self.running:
                logger.debug(
                    "WebSocket manager is already running."
                )
                return

            self.running = True
            self._stop_event.clear()

        self.receiver_thread = threading.Thread(
            target=self._connection_loop,
            name="FlattradeWebSocket",
            daemon=True,
        )

        self.receiver_thread.start()

        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop,
            name="FlattradeWebSocketHeartbeat",
            daemon=True,
        )

        self.heartbeat_thread.start()

        logger.info(
            "Flattrade WebSocket manager started."
        )

    def disconnect(self) -> None:
        """
        Stop the WebSocket connection and background workers.
        """

        with self.lock:

            self.running = False
            self.connected = False
            self.authenticated = False

            self._stop_event.set()

            ws = self.ws

        if ws is not None:

            try:
                ws.close()

            except Exception as exc:

                logger.debug(
                    "WebSocket close failed: %s",
                    exc,
                )

        logger.info(
            "Flattrade WebSocket manager stopped."
        )

    # ==========================================================
    # Connection Loop
    # ==========================================================

    def _connection_loop(self) -> None:
        """
        Maintain the WebSocket connection.

        If the connection is lost while the manager is running,
        reconnect automatically.
        """

        while self.running:

            try:

                logger.info(
                    "Connecting to Flattrade WebSocket: %s",
                    WEBSOCKET_URL,
                )

                self.ws = WebSocketApp(
                    WEBSOCKET_URL,
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                )

                self.ws.run_forever()

            except Exception as exc:

                logger.exception(
                    "Flattrade WebSocket crashed: %s",
                    exc,
                )

            finally:

                with self.lock:

                    self.connected = False
                    self.authenticated = False

            if not self.running:
                break

            logger.warning(
                "WebSocket disconnected. "
                "Reconnecting in %s seconds...",
                self.reconnect_delay,
            )

            self._stop_event.wait(
                self.reconnect_delay
            )

    # ==========================================================
    # WebSocket Callbacks
    # ==========================================================

    def _on_open(
        self,
        ws: WebSocketApp,
    ) -> None:
        """
        Called when the TCP/WebSocket connection is established.

        Flattrade V2 requires an authentication message immediately
        after connection.
        """

        logger.info(
            "Flattrade WebSocket connected."
        )

        with self.lock:

            self.connected = True
            self.authenticated = False
            self.last_heartbeat = time.time()

        self._send_authentication()

    def _on_close(
        self,
        ws: WebSocketApp,
        close_status_code: int | None,
        close_msg: str | None,
    ) -> None:

        logger.warning(
            "Flattrade WebSocket disconnected "
            "(code=%s, message=%s).",
            close_status_code,
            close_msg,
        )

        with self.lock:

            self.connected = False
            self.authenticated = False

    def _on_error(
        self,
        ws: WebSocketApp,
        error: Any,
    ) -> None:

        logger.error(
            "Flattrade WebSocket error: %s",
            error,
        )

    def _on_message(
        self,
        ws: WebSocketApp,
        message: str,
    ) -> None:
        """
        Process one incoming Flattrade WebSocket message.
        """

        self.last_tick = time.time()

        try:

            payload = json.loads(message)

        except json.JSONDecodeError:

            logger.warning(
                "Received non-JSON WebSocket message: %s",
                message,
            )

            return

        if not isinstance(payload, dict):

            logger.debug(
                "Ignoring non-dictionary WebSocket payload: %s",
                payload,
            )

            return

        message_type = payload.get("t")

        # ------------------------------------------------------
        # Authentication acknowledgement
        # ------------------------------------------------------

        if message_type == "ak":

            status = str(
                payload.get("s", "")
            ).lower()

            if status == "ok":

                with self.lock:
                    self.authenticated = True

                logger.info(
                    "Flattrade WebSocket authentication successful."
                )

                self._restore_subscriptions()

            else:

                logger.error(
                    "Flattrade WebSocket authentication failed: %s",
                    payload,
                )

                with self.lock:
                    self.authenticated = False

            return

        # ------------------------------------------------------
        # Touchline acknowledgement
        # ------------------------------------------------------

        if message_type == "tk":

            logger.debug(
                "Touchline subscription acknowledgement: %s",
                payload,
            )

            self._dispatch_tick(payload)

            return

        # ------------------------------------------------------
        # Touchline feed
        # ------------------------------------------------------

        if message_type == "tf":

            self._dispatch_tick(payload)

            return

        # ------------------------------------------------------
        # Touchline unsubscribe acknowledgement
        # ------------------------------------------------------

        if message_type == "uk":

            logger.debug(
                "Touchline unsubscribe acknowledgement: %s",
                payload,
            )

            return

        # ------------------------------------------------------
        # Heartbeat acknowledgement
        # ------------------------------------------------------

        if message_type == "hk":

            self.last_heartbeat = time.time()

            logger.debug(
                "Flattrade heartbeat acknowledgement: %s",
                payload,
            )

            return

        # ------------------------------------------------------
        # Depth feed
        #
        # Not actively subscribed by this first implementation,
        # but keep the message visible for future expansion.
        # ------------------------------------------------------

        if message_type in {
            "df",
            "dk",
            "udk",
        }:

            logger.debug(
                "Flattrade depth message: %s",
                payload,
            )

            return

        # ------------------------------------------------------
        # Order / position messages
        #
        # These will be connected to dedicated callbacks later.
        # ------------------------------------------------------

        if message_type in {
            "om",
            "ok",
            "omsg",
            "pk",
            "upk",
        }:

            logger.debug(
                "Flattrade account WebSocket message: %s",
                payload,
            )

            return

        # ------------------------------------------------------
        # Unknown message
        # ------------------------------------------------------

        logger.debug(
            "Unhandled Flattrade WebSocket message: %s",
            payload,
        )

    # ==========================================================
    # Authentication
    # ==========================================================

    def _send_authentication(self) -> None:
        """
        Send the Flattrade API V2 WebSocket authentication request.
        """

        payload = {
            "t": "a",
            "uid": self.client_id,
            "actid": self.client_id,
            "source": "API",
            "accesstoken": self.access_token,
        }

        self._send(payload)

        logger.debug(
            "Flattrade WebSocket authentication request sent."
        )

    # ==========================================================
    # Sending
    # ==========================================================

    def _send(
        self,
        payload: dict[str, Any],
    ) -> bool:
        """
        Thread-safe JSON send.

        Returns True when the payload was sent successfully.
        """

        with self.lock:

            ws = self.ws

            if ws is None:
                logger.warning(
                    "Cannot send WebSocket message: socket is None."
                )

                return False

            if not self.connected:
                logger.warning(
                    "Cannot send WebSocket message: socket is disconnected."
                )

                return False

            try:

                message = json.dumps(
                    payload,
                    separators=(
                        ",",
                        ":",
                    ),
                )

                ws.send(message)

                return True

            except Exception as exc:

                logger.error(
                    "Failed to send WebSocket message: %s",
                    exc,
                )

                return False

    # ==========================================================
    # Touchline Subscription
    # ==========================================================

    def subscribe(
        self,
        symbols: list[str],
    ) -> None:
        """
        Subscribe to Flattrade touchline market data.

        Example:

            ["NSE|2885"]

        Multiple symbols are sent as:

            NSE|2885#NSE|3045
        """

        if not symbols:
            return

        cleaned_symbols = {
            str(symbol).strip()
            for symbol in symbols
            if str(symbol).strip()
        }

        if not cleaned_symbols:
            return

        with self.lock:

            self.subscriptions.update(
                cleaned_symbols
            )

            ready = (
                self.connected
                and self.authenticated
            )

        if not ready:

            logger.info(
                "Stored %s subscription(s); "
                "WebSocket is not authenticated yet.",
                len(cleaned_symbols),
            )

            return

        self._send_touchline_subscription(
            sorted(cleaned_symbols)
        )

    def unsubscribe(
        self,
        symbols: list[str],
    ) -> None:
        """
        Unsubscribe from Flattrade touchline market data.
        """

        if not symbols:
            return

        cleaned_symbols = {
            str(symbol).strip()
            for symbol in symbols
            if str(symbol).strip()
        }

        if not cleaned_symbols:
            return

        with self.lock:

            self.subscriptions.difference_update(
                cleaned_symbols
            )

            ready = (
                self.connected
                and self.authenticated
            )

        if not ready:

            return

        self._send_touchline_unsubscription(
            sorted(cleaned_symbols)
        )

    def _send_touchline_subscription(
        self,
        symbols: list[str],
    ) -> None:
        """
        Send Flattrade touchline subscription request.
        """

        if not symbols:
            return

        payload = {
            "t": "t",
            "k": "#".join(symbols),
        }

        if self._send(payload):

            logger.info(
                "Subscribed to market data: %s",
                symbols,
            )

    def _send_touchline_unsubscription(
        self,
        symbols: list[str],
    ) -> None:
        """
        Send Flattrade touchline unsubscribe request.
        """

        if not symbols:
            return

        payload = {
            "t": "u",
            "k": "#".join(symbols),
        }

        if self._send(payload):

            logger.info(
                "Unsubscribed from market data: %s",
                symbols,
            )

    def _restore_subscriptions(self) -> None:
        """
        Restore all requested subscriptions after reconnect.
        """

        with self.lock:

            symbols = sorted(
                self.subscriptions
            )

        if not symbols:

            logger.debug(
                "No market subscriptions to restore."
            )

            return

        logger.info(
            "Restoring %s market subscription(s).",
            len(symbols),
        )

        self._send_touchline_subscription(
            symbols
        )

    # ==========================================================
    # Heartbeat
    # ==========================================================

    def _heartbeat_loop(self) -> None:
        """
        Send Flattrade heartbeat every HEARTBEAT_SECONDS.

        Current Flattrade documentation specifies a 30-second
        heartbeat interval.
        """

        while self.running:

            if self._stop_event.wait(
                HEARTBEAT_SECONDS
            ):

                break

            with self.lock:

                ready = (
                    self.connected
                    and self.authenticated
                )

            if not ready:

                continue

            payload = {
                "t": "h",
            }

            if self._send(payload):

                self.last_heartbeat = time.time()

                logger.debug(
                    "Flattrade heartbeat sent."
                )

    def heartbeat(self) -> None:
        """
        Manually send a heartbeat.

        Useful for testing and future health monitoring.
        """

        with self.lock:

            ready = (
                self.connected
                and self.authenticated
            )

        if not ready:

            return

        if self._send(
            {
                "t": "h",
            }
        ):

            self.last_heartbeat = time.time()

    # ==========================================================
    # Tick Dispatch
    # ==========================================================

    def _dispatch_tick(
        self,
        payload: dict[str, Any],
    ) -> None:
        """
        Forward a realtime market message to AEGIS.

        The broker payload is preserved. A future normalization
        layer can convert it into the canonical AEGIS tick model.
        """

        if self.on_tick is None:

            return

        try:

            self.on_tick(payload)

        except Exception as exc:

            logger.exception(
                "Tick callback failed: %s",
                exc,
            )

    # ==========================================================
    # Status
    # ==========================================================

    @property
    def is_connected(self) -> bool:
        """
        Return current socket connection state.
        """

        with self.lock:
            return self.connected

    @property
    def is_authenticated(self) -> bool:
        """
        Return current WebSocket authentication state.
        """

        with self.lock:
            return self.authenticated

    @property
    def subscription_count(self) -> int:
        """
        Return number of currently requested subscriptions.
        """

        with self.lock:
            return len(self.subscriptions)

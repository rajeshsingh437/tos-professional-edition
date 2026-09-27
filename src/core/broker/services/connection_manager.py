"""
AEGIS

Broker Connection Manager

Provides broker-independent connection lifecycle management.

Responsibilities
----------------
- Connection lifecycle state
- Start / stop control
- Automatic reconnect timing
- Thread-safe running state
- Stop signalling

The actual broker WebSocket protocol remains outside this class.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable


logger = logging.getLogger(__name__)


class ConnectionManager:
    """
    Generic connection lifecycle manager.

    This class does not know anything about Flattrade,
    WebSocket protocol messages, authentication, or subscriptions.

    It manages only the lifecycle around a connection worker.
    """

    def __init__(
        self,
        connect_callback: Callable[[], None],
        reconnect_delay: float = 5.0,
    ) -> None:

        if not callable(connect_callback):
            raise ValueError(
                "connect_callback must be callable."
            )

        self.connect_callback = connect_callback
        self.reconnect_delay = reconnect_delay

        self.running = False
        self.connected = False

        self.lock = threading.RLock()

        self._stop_event = threading.Event()

        self.thread: threading.Thread | None = None

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self) -> None:
        """
        Start the connection lifecycle worker.

        Calling start() more than once is safe.
        """

        with self.lock:

            if self.running:

                logger.debug(
                    "Connection manager is already running."
                )

                return

            self.running = True
            self._stop_event.clear()

        self.thread = threading.Thread(
            target=self._run,
            name="AEGISConnectionManager",
            daemon=True,
        )

        self.thread.start()

        logger.info(
            "Connection manager started."
        )

    def stop(self) -> None:
        """
        Stop the connection lifecycle worker.
        """

        with self.lock:

            self.running = False
            self.connected = False

            self._stop_event.set()

        logger.info(
            "Connection manager stopped."
        )

    # ==========================================================
    # Worker
    # ==========================================================

    def _run(self) -> None:
        """
        Maintain the connection while the manager is running.

        The supplied callback performs the actual connection work.
        """

        while self.running:

            try:

                self.connect_callback()

            except Exception as exc:

                logger.exception(
                    "Connection worker failed: %s",
                    exc,
                )

            if not self.running:

                break

            logger.warning(
                "Connection lost. "
                "Reconnecting in %s seconds...",
                self.reconnect_delay,
            )

            self._stop_event.wait(
                self.reconnect_delay
            )

    # ==========================================================
    # State
    # ==========================================================

    def mark_connected(self) -> None:
        """
        Mark the underlying connection as active.
        """

        with self.lock:

            self.connected = True

    def mark_disconnected(self) -> None:
        """
        Mark the underlying connection as inactive.
        """

        with self.lock:

            self.connected = False

    @property
    def is_running(self) -> bool:
        """
        Return whether the lifecycle manager is running.
        """

        with self.lock:

            return self.running

    @property
    def is_connected(self) -> bool:
        """
        Return whether the underlying connection is active.
        """

        with self.lock:

            return self.connected

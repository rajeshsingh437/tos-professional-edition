"""
AEGIS

Broker Heartbeat Service

Provides broker-independent heartbeat scheduling.

Responsibilities
----------------
- Heartbeat scheduling
- Stop/start lifecycle
- Thread-safe execution
- Delegating the actual heartbeat operation
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable


logger = logging.getLogger(__name__)


class HeartbeatService:
    """
    Generic heartbeat scheduler.

    The service does not know broker-specific heartbeat protocol.
    The supplied callback performs the actual heartbeat operation.
    """

    def __init__(
        self,
        heartbeat_callback: Callable[[], None],
        interval: float,
    ) -> None:

        if not callable(heartbeat_callback):
            raise ValueError(
                "heartbeat_callback must be callable."
            )

        if interval <= 0:
            raise ValueError(
                "Heartbeat interval must be greater than zero."
            )

        self.heartbeat_callback = heartbeat_callback
        self.interval = interval

        self.running = False

        self.lock = threading.RLock()

        self._stop_event = threading.Event()

        self.thread: threading.Thread | None = None

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self) -> None:
        """
        Start the heartbeat worker.

        Calling start() more than once is safe.
        """

        with self.lock:

            if self.running:

                logger.debug(
                    "Heartbeat service is already running."
                )

                return

            self.running = True
            self._stop_event.clear()

        self.thread = threading.Thread(
            target=self._run,
            name="AEGISHeartbeat",
            daemon=True,
        )

        self.thread.start()

        logger.info(
            "Heartbeat service started."
        )

    def stop(self) -> None:
        """
        Stop the heartbeat worker.
        """

        with self.lock:

            self.running = False
            self._stop_event.set()

        logger.info(
            "Heartbeat service stopped."
        )

    # ==========================================================
    # Worker
    # ==========================================================

    def _run(self) -> None:
        """
        Execute the heartbeat callback at the configured interval.
        """

        while self.running:

            if self._stop_event.wait(
                self.interval
            ):

                break

            if not self.running:

                break

            try:

                self.heartbeat_callback()

            except Exception as exc:

                logger.exception(
                    "Heartbeat callback failed: %s",
                    exc,
                )

    # ==========================================================
    # Manual Heartbeat
    # ==========================================================

    def send_now(self) -> None:
        """
        Execute one heartbeat immediately.
        """

        with self.lock:

            if not self.running:

                return

        try:

            self.heartbeat_callback()

        except Exception as exc:

            logger.exception(
                "Manual heartbeat failed: %s",
                exc,
            )

    # ==========================================================
    # Status
    # ==========================================================

    @property
    def is_running(self) -> bool:
        """
        Return whether the heartbeat service is running.
        """

        with self.lock:

            return self.running

"""
AEGIS

Market Data Service

Phase 1 — Canonical realtime market-data consumer.

Consumes canonical MarketTick events from the shared EventBus
and maintains the latest known tick for each instrument.

Responsibilities
----------------
- Subscribe to canonical market.tick events
- Maintain latest tick state
- Provide latest tick by exchange/token
- Provide all latest ticks
- Track received tick count

This service does not:
- Connect directly to a broker
- Normalize broker payloads
- Publish broker-specific payloads
- Modify UI state
- Persist market ticks

Architecture
------------

Broker WebSocket
        ↓
FlattradeAdapter
        ↓
TickNormalizer
        ↓
MarketTick
        ↓
Shared EventBus
        ↓
MarketDataService
"""

from __future__ import annotations

from typing import Any

from src.core.events.event_bus import EventBus
from src.core.events.market_tick import MarketTick


class MarketDataService:
    """
    Central consumer of canonical realtime market ticks.
    """

    EVENT_TYPE = "market.tick"

    def __init__(
        self,
        event_bus: EventBus,
    ) -> None:

        self.event_bus = event_bus

        self._latest_ticks: dict[
            tuple[str, str],
            MarketTick,
        ] = {}

        self._tick_count = 0

        self.event_bus.subscribe(
            self.EVENT_TYPE,
            self._handle_tick,
        )

    # ==========================================================
    # Event Handler
    # ==========================================================

    def _handle_tick(
        self,
        tick: MarketTick,
    ) -> None:
        """
        Consume one canonical MarketTick.
        """

        if not isinstance(
            tick,
            MarketTick,
        ):
            raise TypeError(
                "MarketDataService received "
                "an invalid market tick."
            )

        key = (
            tick.exchange,
            tick.token,
        )

        self._latest_ticks[key] = tick

        self._tick_count += 1

    # ==========================================================
    # Latest Tick
    # ==========================================================

    def get_latest(
        self,
        exchange: str,
        token: str,
    ) -> MarketTick | None:
        """
        Return the latest tick for one instrument.
        """

        return self._latest_ticks.get(
            (
                exchange,
                token,
            )
        )

    # ==========================================================
    # All Latest Ticks
    # ==========================================================

    def get_all_latest(
        self,
    ) -> dict[tuple[str, str], MarketTick]:
        """
        Return a snapshot of the latest tick for every
        instrument currently known.
        """

        return dict(
            self._latest_ticks
        )

    # ==========================================================
    # Statistics
    # ==========================================================

    @property
    def tick_count(
        self,
    ) -> int:
        """
        Return the total number of canonical ticks received.
        """

        return self._tick_count

    @property
    def instrument_count(
        self,
    ) -> int:
        """
        Return the number of instruments currently tracked.
        """

        return len(
            self._latest_ticks
        )

    # ==========================================================
    # Snapshot
    # ==========================================================

    def snapshot(
        self,
    ) -> dict[str, Any]:
        """
        Return a lightweight service status snapshot.
        """

        return {
            "event_type": self.EVENT_TYPE,
            "tick_count": self._tick_count,
            "instrument_count": len(
                self._latest_ticks
            ),
        }

    # ==========================================================
    # Shutdown
    # ==========================================================

    def close(
        self,
    ) -> None:
        """
        Unsubscribe from the EventBus.
        """

        self.event_bus.unsubscribe(
            self.EVENT_TYPE,
            self._handle_tick,
        )
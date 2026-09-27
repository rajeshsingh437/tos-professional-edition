"""
AEGIS

Canonical realtime market event.

This module defines the broker-independent market tick contract used
above broker adapters and below higher AEGIS engines.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from types import MappingProxyType
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class MarketTick:
    """
    Canonical broker-independent realtime market event.

    Important identity rule:

    - token is the authoritative broker instrument identity.
    - symbol is optional and must never be fabricated from token.
    - event_time represents the market/broker event timestamp when
      supplied by the broker.
    - received_at represents when AEGIS received the event.

    Raw broker payload remains available through ``raw`` for
    diagnostics and audit, but higher AEGIS layers should consume
    the canonical fields above.
    """

    # =====================================================
    # Event identity
    # =====================================================

    event_type: str
    source: str
    exchange: str
    token: str

    # =====================================================
    # Market value
    # =====================================================

    last_price: Decimal

    # =====================================================
    # AEGIS receipt time
    # =====================================================

    received_at: datetime

    # =====================================================
    # Optional instrument identity
    # =====================================================

    symbol: str | None = None

    # =====================================================
    # Broker/event timestamp
    # =====================================================

    event_time: datetime | None = None

    # =====================================================
    # Optional market fields
    # =====================================================

    previous_close: Decimal | None = None
    volume: int | None = None

    bid: Decimal | None = None
    ask: Decimal | None = None

    bid_quantity: int | None = None
    ask_quantity: int | None = None

    # =====================================================
    # Raw broker evidence
    # =====================================================

    raw: Mapping[str, Any] | None = None

    # =====================================================
    # Validation
    # =====================================================

    def __post_init__(self) -> None:
        """
        Validate the canonical event and preserve raw broker evidence
        without allowing mutation.
        """

        if not self.exchange:
            raise ValueError(
                "MarketTick.exchange cannot be empty"
            )

        if not self.token:
            raise ValueError(
                "MarketTick.token cannot be empty"
            )

        if self.received_at.tzinfo is None:
            raise ValueError(
                "MarketTick.received_at must be timezone-aware"
            )

        if (
            self.event_time is not None
            and self.event_time.tzinfo is None
        ):
            raise ValueError(
                "MarketTick.event_time must be timezone-aware"
            )

        if self.last_price < 0:
            raise ValueError(
                "MarketTick.last_price cannot be negative"
            )

        if (
            self.previous_close is not None
            and self.previous_close < 0
        ):
            raise ValueError(
                "MarketTick.previous_close cannot be negative"
            )

        for name, value in (
            ("bid", self.bid),
            ("ask", self.ask),
        ):
            if value is not None and value < 0:
                raise ValueError(
                    f"MarketTick.{name} cannot be negative"
                )

        for name, value in (
            ("volume", self.volume),
            ("bid_quantity", self.bid_quantity),
            ("ask_quantity", self.ask_quantity),
        ):
            if value is not None and value < 0:
                raise ValueError(
                    f"MarketTick.{name} cannot be negative"
                )

        if self.raw is not None:
            object.__setattr__(
                self,
                "raw",
                MappingProxyType(dict(self.raw)),
            )

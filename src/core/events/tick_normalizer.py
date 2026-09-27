"""
AEGIS

Canonical Realtime Tick Normalizer

Converts broker realtime payloads into the canonical
AEGIS MarketTick contract.

The normalizer is deliberately conservative:
- broker values are converted, not invented;
- unresolved symbol identity remains unresolved;
- raw broker payload is preserved;
- EventBus integration remains outside this component.
"""

from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from src.core.events.market_tick import MarketTick


class TickNormalizer:
    """
    Convert supported realtime broker payloads into MarketTick.

    The current supported raw payload contract is the verified
    Flattrade touchline-style payload.
    """

    SOURCE = "flattrade"
    EVENT_TYPE = "market.tick"

    def normalize(
        self,
        payload: Mapping[str, Any],
        *,
        received_at: datetime | None = None,
    ) -> MarketTick:
        """
        Normalize one raw Flattrade realtime payload.

        Required:
            e  -> exchange
            tk -> broker token
            lp -> last traded price

        Optional:
            pc  -> previous close
            v   -> volume
            bp1 -> best bid
            sp1 -> best ask
            bq1 -> best bid quantity
            sq1 -> best ask quantity

        Symbol identity is intentionally not derived from the token.
        """

        if not isinstance(payload, Mapping):
            raise TypeError("Realtime tick payload must be a mapping.")

        exchange = self._required_text(
            payload,
            "e",
            "exchange",
        )

        token = self._required_text(
            payload,
            "tk",
            "token",
        )

        last_price = self._required_decimal(
            payload,
            "lp",
            "last_price",
        )

        receipt_time = self._normalize_received_at(
            received_at
        )

        event_time = self._extract_event_time(payload)

        return MarketTick(
            event_type=self.EVENT_TYPE,
            source=self.SOURCE,
            exchange=exchange,
            token=token,
            last_price=last_price,
            received_at=receipt_time,
            symbol=self._optional_text(payload, "symbol"),
            event_time=event_time,
            previous_close=self._optional_decimal(
                payload,
                "c",
            ),
            volume=self._optional_int(
                payload,
                "v",
            ),
            bid=self._optional_decimal(
                payload,
                "bp1",
            ),
            ask=self._optional_decimal(
                payload,
                "sp1",
            ),
            bid_quantity=self._optional_int(
                payload,
                "bq1",
            ),
            ask_quantity=self._optional_int(
                payload,
                "sq1",
            ),
            raw=dict(payload),
        )

    # =====================================================
    # Required values
    # =====================================================

    @staticmethod
    def _required_text(
        payload: Mapping[str, Any],
        key: str,
        field_name: str,
    ) -> str:
        value = payload.get(key)

        if value is None:
            raise ValueError(
                f"Realtime tick is missing required field: {field_name}"
            )

        text = str(value).strip()

        if not text:
            raise ValueError(
                f"Realtime tick contains empty required field: {field_name}"
            )

        return text

    @staticmethod
    def _required_decimal(
        payload: Mapping[str, Any],
        key: str,
        field_name: str,
    ) -> Decimal:
        value = payload.get(key)

        if value is None:
            raise ValueError(
                f"Realtime tick is missing required field: {field_name}"
            )

        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid decimal value for {field_name}: {value!r}"
            ) from exc

    # =====================================================
    # Optional numeric values
    # =====================================================

    @staticmethod
    def _optional_decimal(
        payload: Mapping[str, Any],
        key: str,
    ) -> Decimal | None:
        value = payload.get(key)

        if value is None or value == "":
            return None

        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return None

    @staticmethod
    def _optional_int(
        payload: Mapping[str, Any],
        key: str,
    ) -> int | None:
        value = payload.get(key)

        if value is None or value == "":
            return None

        try:
            return int(float(str(value)))
        except (ValueError, TypeError):
            return None

    # =====================================================
    # Optional text
    # =====================================================

    @staticmethod
    def _optional_text(
        payload: Mapping[str, Any],
        key: str,
    ) -> str | None:
        value = payload.get(key)

        if value is None:
            return None

        text = str(value).strip()

        return text or None

    # =====================================================
    # Timestamps
    # =====================================================

    @staticmethod
    def _normalize_received_at(
        value: datetime | None,
    ) -> datetime:
        if value is None:
            return datetime.now(timezone.utc)

        if value.tzinfo is None:
            raise ValueError(
                "received_at must be timezone-aware."
            )

        return value

    @classmethod
    def _extract_event_time(
        cls,
        payload: Mapping[str, Any],
    ) -> datetime | None:
        """
        Extract an event timestamp only when the broker payload
        explicitly provides one.

        No timestamp is fabricated when the payload does not contain
        an identifiable event-time field.
        """

        for key in (
            "ft",
            "event_time",
            "timestamp",
            "ts",
        ):
            value = payload.get(key)

            if value is None or value == "":
                continue

            parsed = cls._parse_event_time(value)

            if parsed is not None:
                return parsed

        return None

    @staticmethod
    def _parse_event_time(
        value: Any,
    ) -> datetime | None:
        if isinstance(value, datetime):
            if value.tzinfo is None:
                return None

            return value

        text = str(value).strip()

        if not text:
            return None

        # ISO-8601 representation.
        try:
            parsed = datetime.fromisoformat(
                text.replace("Z", "+00:00")
            )

            if parsed.tzinfo is not None:
                return parsed

        except ValueError:
            pass

        # Numeric epoch representation.
        try:
            numeric = float(text)

            # Millisecond epoch.
            if numeric > 10_000_000_000:
                numeric /= 1000.0

            return datetime.fromtimestamp(
                numeric,
                tz=timezone.utc,
            )

        except (ValueError, OverflowError, OSError):
            return None

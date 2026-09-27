"""Read-only Flattrade REST API client."""

from __future__ import annotations

import json
from typing import Any

import requests

from brokers.flattrade.constants import API_BASE_URL, REQUEST_TIMEOUT


class RestClientError(RuntimeError):
    """Raised when a Flattrade REST request fails."""


class RestClient:
    """Execute authenticated, read-only Flattrade API requests."""

    def __init__(
        self,
        access_token: str,
        client_id: str,
    ) -> None:
        self.access_token = access_token
        self.client_id = client_id
        self.session = requests.Session()

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Send an authenticated Flattrade POST request."""
        if not self.access_token:
            raise RestClientError("A Flattrade access token is required")
        if not self.client_id:
            raise RestClientError("A Flattrade client ID is required")

        try:
            payload_str = f"jData={json.dumps(payload)}&jKey={self.access_token}"
            response = self.session.post(
                f"{API_BASE_URL}/{endpoint}",
                data=payload_str,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
        except requests.RequestException as error:
            raise RestClientError(
                f"Flattrade {endpoint} request failed: {error}"
            ) from error

        try:
            result = response.json()
        except ValueError as error:
            raise RestClientError(
                f"Flattrade {endpoint} returned invalid JSON"
            ) from error

        if isinstance(result, dict) and result.get("stat") == "Not_Ok":
            message = str(result.get("emsg") or f"Flattrade {endpoint} failed")
            if endpoint in ("OrderBook", "TradeBook", "PositionBook", "Holdings") and "no data" in message.lower():
                return []
            raise RestClientError(message)

        if not isinstance(result, (dict, list)):
            raise RestClientError(
                f"Flattrade {endpoint} returned an unexpected response"
            )

        return result

    def _account_payload(self, **values: Any) -> dict[str, Any]:
        """Build a payload containing the required account identifiers."""
        return {
            "uid": self.client_id,
            "actid": self.client_id,
            **values,
        }

    def _order_payload(self, **values: Any) -> dict[str, Any]:
        """
        Build a payload for Flattrade order APIs.

        All order requests automatically include the required account
        identifiers (uid and actid). Additional order-specific fields
        are supplied via keyword arguments.
        """
        return self._account_payload(**values)

    def _order_request(
        self,
        endpoint: str,
        **values: Any,
    ) -> dict[str, Any]:
        """
        Execute an order-management request.
        """

        result = self.post(
            endpoint,
            self._order_payload(**values),
        )

        return self._as_dict(result, endpoint)

    def get_limits(self) -> dict[str, Any]:
        """Fetch available funds and account limits."""
        result = self.post("Limits", self._account_payload())
        return self._as_dict(result, "Limits")

    def get_holdings(self) -> list[dict[str, Any]]:
        """Fetch cash-equity holdings."""
        result = self.post(
            "Holdings",
            self._account_payload(prd="C"),
        )
        return self._as_list(result, "Holdings")

    def get_positions(self) -> list[dict[str, Any]]:
        """Fetch current positions."""
        result = self.post("PositionBook", self._account_payload())
        return self._as_list(result, "PositionBook")

    def get_orders(self) -> list[dict[str, Any]]:
        """Fetch the order book."""
        result = self.post("OrderBook", self._account_payload())
        return self._as_list(result, "OrderBook")

    def get_tradebook(self) -> list[dict[str, Any]]:
        """Fetch the trade book."""
        result = self.post("TradeBook", self._account_payload())
        return self._as_list(result, "TradeBook")

    # ============================================================
    # Order APIs
    # ============================================================

    def place_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:
        """Wrapper around Flattrade PlaceOrder API."""

        result = self.post(
            "PlaceOrder",
            self._order_payload(**values),
        )

        return self._as_dict(result, "PlaceOrder")

    def modify_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:
        """Wrapper around Flattrade ModifyOrder API."""

        result = self.post(
            "ModifyOrder",
            self._order_payload(**values),
        )

        return self._as_dict(result, "ModifyOrder")

    def cancel_order(
        self,
        orderno: str,
    ) -> dict[str, Any]:
        """Wrapper around Flattrade CancelOrder API."""

        result = self.post(
            "CancelOrder",
            self._order_payload(
                norenordno=orderno,
            ),
        )

        return self._as_dict(result, "CancelOrder")

    # ============================================================
    # Market Data APIs
    # ============================================================

    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        """Search instruments."""

        result = self.post(
            "SearchScrip",
            {
                "uid": self.client_id,
                "stext": text,
            },
        )

        return self._as_list(result, "SearchScrip")

    def get_quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:
        """Fetch a live market quote."""

        result = self.post(
            "GetQuotes",
            {
                "uid": self.client_id,
                "exch": exchange,
                "token": symbol,
            },
        )

        return self._as_dict(result, "GetQuotes")

    def get_option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:
        """Fetch option chain."""

        result = self.post(
            "GetOptionChain",
            {
                "uid": self.client_id,
                "tsym": symbol,
                "expiry": expiry,
            },
        )

        return self._as_dict(result, "GetOptionChain")

    def get_historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> list[dict[str, Any]]:
        """Fetch historical candles."""

        result = self.post(
            "TPSeries",
            {
                "uid": self.client_id,
                "exch": exchange,
                "token": symbol,
                "intrv": interval,
                "st": start,
                "et": end,
            },
        )

        return self._as_list(result, "TPSeries")

    @staticmethod
    def _as_dict(
        result: dict[str, Any] | list[dict[str, Any]],
        endpoint: str,
    ) -> dict[str, Any]:
        """Return a dictionary result or raise a clear response error."""
        if isinstance(result, dict):
            return result
        raise RestClientError(
            f"Flattrade {endpoint} returned a list, not an object"
        )

    @staticmethod
    def _as_list(
        result: dict[str, Any] | list[dict[str, Any]],
        endpoint: str,
    ) -> list[dict[str, Any]]:
        """Return a list result or raise a clear response error."""
        if isinstance(result, list):
            return result
        raise RestClientError(
            f"Flattrade {endpoint} returned an object, not a list"
        )

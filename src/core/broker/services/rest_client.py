"""
AEGIS

Read-only Flattrade REST API Client
"""

from __future__ import annotations

import json
from typing import Any

import requests

from src.core.broker.constants import (
    API_BASE_URL,
    REQUEST_TIMEOUT,
)


class RestClientError(RuntimeError):
    """
    Raised when a REST request fails.
    """


class RestClient:
    """
    Authenticated Flattrade REST client.
    """

    def __init__(
        self,
        access_token: str,
        client_id: str,
    ) -> None:

        if not access_token:
            raise RestClientError(
                "Access token is required."
            )

        if not client_id:
            raise RestClientError(
                "Client ID is required."
            )

        self.access_token = access_token
        self.client_id = client_id

        self.session = requests.Session()

    # ==========================================================
    # Generic POST
    # ==========================================================

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any] | list[dict[str, Any]]:

        try:

            response = self.session.post(
                f"{API_BASE_URL}/{endpoint}",
                data={
                    "jData": json.dumps(payload),
                    "jKey": self.access_token,
                },
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException as error:

            raise RestClientError(
                f"{endpoint} request failed."
            ) from error

        try:

            result = response.json()

        except ValueError as error:

            raise RestClientError(
                "Broker returned invalid JSON."
            ) from error

        if (
            isinstance(result, dict)
            and result.get("stat") == "Not_Ok"
        ):

            raise RestClientError(
                result.get(
                    "emsg",
                    f"{endpoint} failed.",
                )
            )

        if not isinstance(
            result,
            (dict, list),
        ):

            raise RestClientError(
                "Unexpected response type."
            )

        return result

    # ==========================================================
    # Payload Builders
    # ==========================================================

    def _account_payload(
        self,
        **values: Any,
    ) -> dict[str, Any]:

        return {
            "uid": self.client_id,
            "actid": self.client_id,
            **values,
        }

    def _order_payload(
        self,
        **values: Any,
    ) -> dict[str, Any]:

        return self._account_payload(
            **values
        )

    # ==========================================================
    # Response Helpers
    # ==========================================================

    def _as_dict(
        self,
        value: Any,
        endpoint: str,
    ) -> dict[str, Any]:

        if isinstance(
            value,
            dict,
        ):
            return value

        raise RestClientError(
            f"{endpoint} returned invalid data."
        )

    def _as_list(
        self,
        value: Any,
        endpoint: str,
    ) -> list[dict[str, Any]]:

        if isinstance(
            value,
            list,
        ):
            return value

        raise RestClientError(
            f"{endpoint} returned invalid data."
        )
        # ==========================================================
    # Account APIs
    # ==========================================================

    def get_limits(
        self,
    ) -> dict[str, Any]:

        result = self.post(
            "Limits",
            self._account_payload(),
        )

        return self._as_dict(
            result,
            "Limits",
        )

    def get_holdings(
        self,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "Holdings",
            self._account_payload(
                prd="C",
            ),
        )

        return self._as_list(
            result,
            "Holdings",
        )

    def get_positions(
        self,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "PositionBook",
            self._account_payload(),
        )

        return self._as_list(
            result,
            "PositionBook",
        )

    def get_orders(
        self,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "OrderBook",
            self._account_payload(),
        )

        return self._as_list(
            result,
            "OrderBook",
        )

    def get_tradebook(
        self,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "TradeBook",
            self._account_payload(),
        )

        return self._as_list(
            result,
            "TradeBook",
        )

    # ==========================================================
    # Order APIs
    # ==========================================================

    def place_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:

        result = self.post(
            "PlaceOrder",
            self._order_payload(
                **values,
            ),
        )

        return self._as_dict(
            result,
            "PlaceOrder",
        )

    def modify_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:

        result = self.post(
            "ModifyOrder",
            self._order_payload(
                **values,
            ),
        )

        return self._as_dict(
            result,
            "ModifyOrder",
        )

    def cancel_order(
        self,
        orderno: str,
    ) -> dict[str, Any]:

        result = self.post(
            "CancelOrder",
            self._order_payload(
                norenordno=orderno,
            ),
        )

        return self._as_dict(
            result,
            "CancelOrder",
        )
        # ==========================================================
    # Market Data APIs
    # ==========================================================

    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "SearchScrip",
            {
                "uid": self.client_id,
                "stext": text,
            },
        )

        return self._as_list(
            result,
            "SearchScrip",
        )

    def get_quote(
        self,
        exchange: str,
        token: str,
    ) -> dict[str, Any]:

        result = self.post(
            "GetQuotes",
            {
                "uid": self.client_id,
                "exch": exchange,
                "token": token,
            },
        )

        return self._as_dict(
            result,
            "GetQuotes",
        )

    def get_option_chain(
        self,
        exchange: str,
        tradingsymbol: str,
        strike_price: float,
        count: int = 10,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "GetOptionChain",
            {
                "uid": self.client_id,
                "exch": exchange,
                "tsym": tradingsymbol,
                "strprc": strike_price,
                "cnt": count,
            },
        )

        return self._as_list(
            result,
            "GetOptionChain",
        )

    def get_time_price_series(
        self,
        exchange: str,
        token: str,
        start_time: str,
        interval: int,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "TPSeries",
            {
                "uid": self.client_id,
                "exch": exchange,
                "token": token,
                "st": start_time,
                "intrv": interval,
            },
        )

        return self._as_list(
            result,
            "TPSeries",
        )

    # ==========================================================
    # Utility
    # ==========================================================

    def check_connection(self) -> bool:
        """
        Verify authentication by requesting account limits.
        """

        try:

            self.get_limits()

            return True

        except Exception:

            return False
            # ==========================================================
    # Future APIs (Reserved)
    # ==========================================================

    def get_margin(
        self,
    ) -> dict[str, Any]:
        """
        Reserved for future margin APIs.
        """

        raise NotImplementedError

    def get_funds(
        self,
    ) -> dict[str, Any]:
        """
        Reserved for future funds APIs.
        """

        raise NotImplementedError

    def get_order_history(
        self,
        orderno: str,
    ) -> dict[str, Any]:
        """
        Reserved for future order history API.
        """

        raise NotImplementedError

    def get_daily_pnl(
        self,
    ) -> dict[str, Any]:
        """
        Reserved for future analytics.
        """

        raise NotImplementedError

    def close(self) -> None:
        """
        Close HTTP session.
        """

        self.session.close()

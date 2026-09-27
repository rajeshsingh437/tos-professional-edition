"""
AEGIS

Read-only Flattrade REST API Client
"""


from __future__ import annotations
import time

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
            print("***** REST_CLIENT POST EXECUTING *****")

            payload_string = (
                f"jData={json.dumps(payload)}"
                f"&jKey={self.access_token}"
            )

            print("\nOFFICIAL PAYLOAD")
            print("=" * 70)
            print(payload_string)
            print("=" * 70)

            response = self.session.post(
    f"{API_BASE_URL}/{endpoint}",
    data=payload_string,
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
    },
    timeout=REQUEST_TIMEOUT,
            )


            print()
            print("=" * 70)
            print(f"{endpoint} STATUS")
            print("=" * 70)
            print(response.status_code)

            print()
            print("=" * 70)
            print(f"{endpoint} TEXT")
            print("=" * 70)
            print(response.text)
            print("=" * 70)
            print("\n" + "=" * 70)
            print("REQUEST HEADERS")
            print("=" * 70)
            print(response.request.headers)

            print("\nBODY SENT")
            print("=" * 70)
            print(response.request.body)
            print("=" * 70)

            response.raise_for_status()

            result = response.json()

            print("\n" + "=" * 70)
            print(f"{endpoint} RESPONSE")
            print("=" * 70)
            print(result)
            print("=" * 70)

            return result

        except requests.RequestException as exc:
            raise RestClientError(
                f"{endpoint} request failed: {exc}"
            ) from exc

        except ValueError as exc:
            raise RestClientError(
                f"{endpoint} returned invalid JSON."
            ) from exc

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
            ordersource="API",
            **values,
        )

    # ==========================================================
    # Response Helpers
    # ==========================================================

    def _as_dict(
        self,
        value: Any,
        endpoint: str,
    ) -> dict[str, Any]:

        if isinstance(value, dict):
            return value

        raise RestClientError(
            f"{endpoint} returned invalid data."
        )

    def _as_list(
        self,
        value: Any,
        endpoint: str,
    ) -> list[dict[str, Any]]:

        if isinstance(value, list):
            return value

        if isinstance(value, dict):

            if value.get("stat") == "Not_Ok":

                message = (
                    str(value.get("emsg", ""))
                    .lower()
                    .strip()
                )

                if "no data" in message:
                    return []

            if value.get("stat") == "Ok":

                values = value.get("values")

                if isinstance(values, list):
                    return values

                return []

        raise RestClientError(
            f"{endpoint} returned invalid data: {value}"
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
            self._order_payload(**values),
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
            self._order_payload(**values),
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

    def search_symbol(
        self,
        exchange: str,
        searchtext: str,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "SearchScrip",
            {
                "uid": self.client_id,
                "exch": exchange,
                "stext": searchtext,
            },
        )

        return self._as_list(
            result,
            "SearchScrip",
        )

    def get_option_chain(
        self,
        exchange: str,
        tradingsymbol: str,
        strike_price: float,
        count: int = 10,
    ) -> list[dict[str, Any]]:

        result = self.post(
            "OptionChain",
            {
                "uid": self.client_id,
                "exch": exchange,
                "tsym": tradingsymbol,
                "strprc": str(strike_price),
                "cnt": str(count),
            },
        )

        return self._as_list(
            result,
            "OptionChain",
        )

    def get_time_price_series(
        self,
        exchange: str,
        token: str,
        start_time: str,
        interval: int,
    ) -> list[dict[str, Any]]:

        start_timestamp = int(
            time.mktime(
                time.strptime(
                    start_time,
                    "%d-%m-%Y %H:%M:%S",
                )
            )
        )

        result = self.post(
            "TPSeries",
            {
                "uid": self.client_id,
                "exch": exchange,
                "token": token,
                "st": str(start_timestamp),
                "intrv": str(interval),
            },
        )

        return self._as_list(
            result,
            "TPSeries",
        )

    # ==========================================================
    # Health
    # ==========================================================

    def check_connection(
        self,
    ) -> bool:

        try:
            self.get_limits()
        except RestClientError:
            return False

        return True

    # ==========================================================
    # Cleanup
    # ==========================================================

    def close(
        self,
    ) -> None:

        self.session.close()

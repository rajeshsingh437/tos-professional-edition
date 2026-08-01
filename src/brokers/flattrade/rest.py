"""
AEGIS

Flattrade REST Client
"""

from __future__ import annotations

from typing import Any

import requests

from brokers.flattrade.constants import (
    API_BASE_URL,
    REQUEST_TIMEOUT,
)


class RestClient:
    """
    Generic REST client for Flattrade.
    """

    def __init__(self, access_token: str):

        self.access_token = access_token

        self.session = requests.Session()

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Execute POST request.
        """

        response = self.session.post(
            f"{API_BASE_URL}/{endpoint}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        return response.json()

    def get_limits(self):

        raise NotImplementedError

    def get_positions(self):

        raise NotImplementedError

    def get_orders(self):

        raise NotImplementedError

    def get_tradebook(self):

        raise NotImplementedError

    def get_holdings(self):

        raise NotImplementedError

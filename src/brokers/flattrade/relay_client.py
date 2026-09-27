"""
Oracle Relay client.

The desktop never talks directly to Flattrade APIs.
Every authenticated request goes through the Oracle VM relay.
"""

from __future__ import annotations

from typing import Any

import requests


class RelayError(RuntimeError):
    """Raised when the relay cannot complete a request."""


class RelayClient:
    def __init__(
        self,
        relay_url: str,
        shared_secret: str,
    ) -> None:
        self.base_url = relay_url.rstrip("/")
        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization": f"Bearer {shared_secret}",
                "Content-Type": "application/json",
            }
        )

    def complete_login(self, request_code: str) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/complete_login",
            json={"request_code": request_code},
            timeout=20,
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("error"):
            raise RelayError(payload["error"])

        return payload

    def login_status(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/login_status",
            timeout=10,
        )

        response.raise_for_status()
        return response.json()

    def positions(self) -> Any:
        response = self.session.get(
            f"{self.base_url}/positions",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def orders(self) -> Any:
        response = self.session.get(
            f"{self.base_url}/orders",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def trades(self) -> Any:
        response = self.session.get(
            f"{self.base_url}/trades",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def limits(self) -> Any:
        response = self.session.get(
            f"{self.base_url}/limits",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

    def holdings(self) -> Any:
        response = self.session.get(
            f"{self.base_url}/holdings",
            timeout=20,
        )
        response.raise_for_status()
        return response.json()

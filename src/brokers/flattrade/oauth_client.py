"""Flattrade OAuth authorization and token-exchange client."""

from __future__ import annotations

import hashlib
from typing import Any

import requests

from brokers.flattrade.constants import LOGIN_URL, REQUEST_TIMEOUT, TOKEN_URL


class OAuthError(RuntimeError):
    """Raised when Flattrade OAuth authorization or token exchange fails."""


class OAuthClient:
    """Build Flattrade OAuth requests and exchange a request code for a token."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
    ) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()

    @property
    def authorization_url(self) -> str:
        """Return the Flattrade browser-login URL for this API key."""
        return f"{LOGIN_URL}?app_key={self.api_key}"

    def api_secret_hash(self, request_code: str) -> str:
        """Return Flattrade's required SHA-256 security-key hash."""
        value = f"{self.api_key}{request_code}{self.api_secret}"
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def build_payload(self, request_code: str) -> dict[str, str]:
        """Build the token-exchange payload for a request code."""
        if not request_code:
            raise ValueError("request_code is required for token exchange")

        return {
            "api_key": self.api_key,
            "request_code": request_code,
            "api_secret": self.api_secret_hash(request_code),
        }

    def exchange_request_code(
        self,
        request_code: str,
    ) -> dict[str, Any]:
        """Forward a one-time request code to the Oracle Cloud relay server."""

        payload = {"code": request_code}

        print("=" * 60)
        print("RELAY URL:")
        print("http://localhost:8091/complete_login")
        print()
        print("PAYLOAD:")
        print(payload)
        print("=" * 60)

        import os

        relay_secret = os.getenv("RELAY_SHARED_SECRET", "AEGIS_RELAY_2026_SECRET")
        relay_server = os.getenv("RELAY_SERVER_URL", "http://130.210.22.73:8091")

        try:
            response = self.session.post(
                f"{relay_server}/complete_login",
                json=payload,
                headers={"Authorization": f"Bearer {relay_secret}"},
                timeout=REQUEST_TIMEOUT,
            )

            print()
            print("HTTP STATUS:", response.status_code)
            print("RAW RESPONSE:")
            print(response.text)
            print()

            response.raise_for_status()

        except requests.RequestException as error:
            print(f"DEBUG NETWORK ERROR: {type(error).__name__}: {error}")
            raise OAuthError("Unable to connect to the Oracle Cloud relay server") from error

        try:
            resp_payload: dict[str, Any] = response.json()

        except ValueError as error:
            raise OAuthError(
                "Relay returned an invalid response"
            ) from error

        return resp_payload

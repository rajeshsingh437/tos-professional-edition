"""
AEGIS

Flattrade OAuth Client
"""

from __future__ import annotations

import hashlib
from typing import Any

import requests

from ..constants import  (
    LOGIN_URL,
    REQUEST_TIMEOUT,
    TOKEN_URL,
)


class OAuthError(RuntimeError):
    """Raised when Flattrade OAuth fails."""


class OAuthClient:
    """
    Flattrade OAuth helper.
    """

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
        url = f"{LOGIN_URL}?app_key={self.api_key}"

        print("\n========== AUTH URL ==========")
        print(url)
        print("==============================\n")

        return url

    def api_secret_hash(
        self,
        request_code: str,
    ) -> str:
        """
        SHA256 hash required by Flattrade.
        """

        value = (
            f"{self.api_key}"
            f"{request_code}"
            f"{self.api_secret}"
        )

        return hashlib.sha256(
            value.encode("utf-8")
        ).hexdigest()

    def build_payload(
        self,
        request_code: str,
    ) -> dict[str, str]:
        """
        Build token request payload.
        """

        return {
            "api_key": self.api_key,
            "request_code": request_code,
            "api_secret": self.api_secret_hash(
                request_code
            ),
        }

    def exchange_request_code(
        self,
        request_code: str,
    ) -> dict[str, Any]:
        """
        Exchange request code for access token.
        """

        try:
            payload = self.build_payload(request_code)

            print("\n========== TOKEN REQUEST ==========")
            print(payload)
            print("===================================\n")

            response = self.session.post(
                TOKEN_URL,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException as error:
            raise OAuthError(
                "Unable to exchange request code."
            ) from error

        try:
            payload = response.json()

        except ValueError as error:
            raise OAuthError(
                "Invalid OAuth response."
            ) from error

        if (
            payload.get("status") != "Ok"
            or not payload.get("token")
        ):
            raise OAuthError(
                payload.get(
                    "emsg",
                    "OAuth authentication failed.",
                )
            )

        return payload

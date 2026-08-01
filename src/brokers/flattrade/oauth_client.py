"""
AEGIS

Flattrade OAuth Client
"""

from __future__ import annotations

import hashlib


AUTH_URL = "https://authapi.flattrade.in/trade/apitoken"


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

    @property
    def api_secret_hash(self) -> str:
        """
        SHA-256 hash required by Flattrade.
        """

        return hashlib.sha256(
            self.api_secret.encode("utf-8")
        ).hexdigest()

    def build_payload(
        self,
        request_code: str,
    ) -> dict:
        """
        Build authentication payload.
        """

        return {
            "api_key": self.api_key,
            "request_code": request_code,
            "api_secret": self.api_secret_hash,
        }

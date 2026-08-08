"""
AEGIS

Flattrade Authentication Manager
"""

from __future__ import annotations

from dataclasses import dataclass

from config.settings import (
    load_broker,
    load_session,
    save_session,
)


@dataclass
class AuthState:
    """
    Current locally stored authentication state.
    """

    authenticated: bool = False
    access_token: str = ""
    client_id: str = ""


class AuthenticationManager:
    """
    Load, persist and clear authentication session.
    """

    def __init__(self) -> None:

        self.broker = load_broker()
        self.session = load_session()

        access_token = self.session.get(
            "access_token",
            "",
        )

        self.state = AuthState(
            authenticated=bool(access_token),
            access_token=access_token,
            client_id=self.session.get(
                "client_id",
                "",
            ),
        )

    @property
    def is_authenticated(self) -> bool:
        """
        Returns True if an access token exists.
        """

        return self.state.authenticated

    def save_authenticated_session(
        self,
        access_token: str,
        client_id: str = "",
    ) -> None:
        """
        Persist OAuth session.
        """

        if not access_token:
            raise ValueError(
                "access_token is required"
            )

        self.state = AuthState(
            authenticated=True,
            access_token=access_token,
            client_id=client_id,
        )

        self.session = {
            "access_token": access_token,
            "client_id": client_id,
        }

        save_session(self.session)
        print("Authentication session saved.")

    def clear(self) -> None:
        """
        Clear authentication session.
        """

        self.state = AuthState()
        self.session = {}

        save_session(self.session)

        print("Authentication session cleared.")


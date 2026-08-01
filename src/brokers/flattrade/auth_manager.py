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
    Current authentication state.
    """

    authenticated: bool = False
    access_token: str = ""


class AuthenticationManager:
    """
    Controls the Flattrade login lifecycle.
    """

    def __init__(self) -> None:

        self.broker = load_broker()
        self.session = load_session()

        self.state = AuthState(
            authenticated=bool(
                self.session.get("access_token")
            ),
            access_token=self.session.get(
                "access_token",
                "",
            ),
        )

    @property
    def is_authenticated(self) -> bool:
        """
        Returns current login status.
        """

        return self.state.authenticated

    def clear(self) -> None:
        """
        Clear local session.
        """

        self.state = AuthState()

        save_session({})

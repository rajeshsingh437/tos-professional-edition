"""
AEGIS

Broker Session Manager

Owns local broker-session persistence and restoration.

Responsibilities
----------------
- Load the persisted broker session
- Save an authenticated session
- Restore access-token/client-id state
- Clear the persisted session
- Keep session persistence separate from authentication flow
"""

from __future__ import annotations

from dataclasses import dataclass

from config.settings import (
    load_session,
    save_session,
)


@dataclass
class SessionState:
    """
    Persisted broker session state.
    """

    access_token: str = ""
    client_id: str = ""

    @property
    def authenticated(self) -> bool:
        """
        Return True when a usable access token exists.
        """

        return bool(
            self.access_token
            and self.client_id
        )


class SessionManager:
    """
    Manages the locally persisted broker session.

    This service deliberately contains no OAuth logic and no
    broker API communication.
    """

    def __init__(self) -> None:

        self._state = self._load()

    # ==========================================================
    # Load
    # ==========================================================

    def _load(self) -> SessionState:
        """
        Load the persisted session from configuration storage.
        """

        session = load_session()

        if not isinstance(session, dict):
            return SessionState()

        return SessionState(
            access_token=str(
                session.get(
                    "access_token",
                    "",
                )
                or ""
            ),
            client_id=str(
                session.get(
                    "client_id",
                    "",
                )
                or ""
            ),
        )

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def access_token(self) -> str:
        """
        Return the persisted access token.
        """

        return self._state.access_token

    @property
    def client_id(self) -> str:
        """
        Return the persisted client ID.
        """

        return self._state.client_id

    @property
    def is_authenticated(self) -> bool:
        """
        Return whether a complete persisted session exists.
        """

        return self._state.authenticated

    # ==========================================================
    # Save
    # ==========================================================

    def save(
        self,
        access_token: str,
        client_id: str,
    ) -> None:
        """
        Persist an authenticated broker session.
        """

        if not access_token:
            raise ValueError(
                "access_token is required."
            )

        if not client_id:
            raise ValueError(
                "client_id is required."
            )

        self._state = SessionState(
            access_token=access_token,
            client_id=client_id,
        )

        save_session(
            {
                "access_token": access_token,
                "client_id": client_id,
            }
        )

    # ==========================================================
    # Restore
    # ==========================================================

    def restore(self) -> SessionState:
        """
        Return the currently persisted session state.
        """

        return self._state

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self) -> None:
        """
        Remove the persisted broker session.
        """

        self._state = SessionState()

        save_session({})

    # ==========================================================
    # Refresh
    # ==========================================================

    def reload(self) -> SessionState:
        """
        Reload session state from persistent storage.

        Useful when another service has updated the session.
        """

        self._state = self._load()

        return self._state

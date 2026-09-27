"""
AEGIS

Persistence Storage
Phase 1 — Durable application state.

This service provides the central SQLite-backed key/value
persistence layer for AEGIS.

Responsibilities
----------------
- Create and maintain the AEGIS application database
- Store application state as key/value pairs
- Retrieve individual values
- Retrieve all values
- Update existing values
- Remove values
- Clear all application state

The persistence layer is intentionally independent of:
- Broker authentication/session storage
- UI
- Trading Journal
- Event Bus
- SENTRY-specific browser/localStorage code

Those domains will be migrated on top of this foundation
in later phases.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"

DATABASE_PATH = DATA_DIR / "aegis.db"


# ==========================================================
# Persistence Storage
# ==========================================================


class Storage:
    """
    Central SQLite-backed persistence service for AEGIS.
    """

    def __init__(
        self,
        database_path: Path | None = None,
    ) -> None:

        self.database_path = (
            database_path
            if database_path is not None
            else DATABASE_PATH
        )

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    # ======================================================
    # Database
    # ======================================================

    def _connect(self) -> sqlite3.Connection:
        """
        Open a SQLite connection.
        """

        connection = sqlite3.connect(
            self.database_path,
            timeout=10,
        )

        return connection

    def _initialize_database(self) -> None:
        """
        Create the persistence schema if it does not exist.
        """

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS kv_store (
                    key        TEXT PRIMARY KEY,
                    value      TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                               DEFAULT (datetime('now'))
                )
                """
            )

            connection.commit()

    # ======================================================
    # Read
    # ======================================================

    def get_item(
        self,
        key: str,
    ) -> str | None:
        """
        Return the stored value for a key.

        Returns None when the key does not exist.
        """

        if not key:
            raise ValueError(
                "Storage key cannot be empty."
            )

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT value
                FROM kv_store
                WHERE key = ?
                """,
                (key,),
            ).fetchone()

        if row is None:
            return None

        return str(row[0])

    # ======================================================
    # Write
    # ======================================================

    def set_item(
        self,
        key: str,
        value: str,
    ) -> None:
        """
        Save or update a key/value pair.
        """

        if not key:
            raise ValueError(
                "Storage key cannot be empty."
            )

        if not isinstance(value, str):
            raise TypeError(
                "Storage value must be a string."
            )

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO kv_store (
                    key,
                    value,
                    updated_at
                )
                VALUES (
                    ?,
                    ?,
                    datetime('now')
                )
                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (
                    key,
                    value,
                ),
            )

            connection.commit()

    # ======================================================
    # Delete
    # ======================================================

    def remove_item(
        self,
        key: str,
    ) -> None:
        """
        Remove one stored key.
        """

        if not key:
            raise ValueError(
                "Storage key cannot be empty."
            )

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM kv_store
                WHERE key = ?
                """,
                (key,),
            )

            connection.commit()

    # ======================================================
    # Read All
    # ======================================================

    def get_all_items(
        self,
    ) -> dict[str, str]:
        """
        Return every stored key/value pair.
        """

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT key, value
                FROM kv_store
                ORDER BY key
                """
            ).fetchall()

        return {
            str(key): str(value)
            for key, value in rows
        }

    # ======================================================
    # Clear
    # ======================================================

    def clear(self) -> None:
        """
        Remove all application state from the key/value store.
        """

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM kv_store
                """
            )

            connection.commit()

    # ======================================================
    # Health
    # ======================================================

    def check_connection(self) -> bool:
        """
        Verify that the SQLite database is accessible.
        """

        try:

            with self._connect() as connection:

                connection.execute(
                    "SELECT 1"
                ).fetchone()

            return True

        except sqlite3.Error:

            return False


# ==========================================================
# Default Storage Instance
# ==========================================================

storage = Storage()

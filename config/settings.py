"""
AEGIS Configuration

Central configuration manager.
"""

from __future__ import annotations

import json
from pathlib import Path


CONFIG_DIR = Path(__file__).resolve().parent

BROKER_FILE = CONFIG_DIR / "broker.json"
SESSION_FILE = CONFIG_DIR / "session.json"


def load_broker() -> dict:
    """
    Load broker configuration.
    """

    if not BROKER_FILE.exists():
        raise FileNotFoundError(
            f"Broker configuration not found:\n{BROKER_FILE}"
        )

    with BROKER_FILE.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def load_session() -> dict:
    """
    Load saved session.
    """

    if not SESSION_FILE.exists():
        return {}

    with SESSION_FILE.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def save_session(session: dict) -> None:
    """
    Save authenticated session.
    """

    with SESSION_FILE.open("w", encoding="utf-8") as fp:
        json.dump(session, fp, indent=4)


def clear_session() -> None:
    """
    Clear broker session.
    """

    save_session({})

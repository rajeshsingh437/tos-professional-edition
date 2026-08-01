"""
AEGIS Flattrade Adapter

Implements the broker interface for Flattrade.
"""

from __future__ import annotations

from ..broker_interface import IBrokerAdapter


class FlattradeAdapter(IBrokerAdapter):
    """
    Flattrade broker implementation.
    """

    def __init__(self):

        self._connected = False
        self._authenticated = False

    def connect(self) -> bool:

        print("Connecting to Flattrade...")

        self._connected = True

        return True

    def disconnect(self) -> None:

        print("Disconnected.")

        self._connected = False
        self._authenticated = False

    def login(self) -> bool:

        print("Login requested.")

        self._authenticated = True

        return True

    def logout(self) -> None:

        print("Logout requested.")

        self._authenticated = False

    def is_connected(self) -> bool:

        return self._connected

    def subscribe_market_data(self) -> None:

        print("Market subscription.")

    def subscribe_orders(self) -> None:

        print("Order subscription.")

    def subscribe_trades(self) -> None:

        print("Trade subscription.")

    def subscribe_positions(self) -> None:

        print("Position subscription.")

    def get_limits(self):

        return {}

    def get_profile(self):

        return {}

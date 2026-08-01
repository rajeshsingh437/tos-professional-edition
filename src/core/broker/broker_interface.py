"""
AEGIS Broker Interface

Every broker adapter must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class IBrokerAdapter(ABC):
    """
    Base interface for all broker implementations.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Connect to broker."""
        raise NotImplementedError

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from broker."""
        raise NotImplementedError

    @abstractmethod
    def login(self) -> bool:
        """Authenticate broker session."""
        raise NotImplementedError

    @abstractmethod
    def logout(self) -> None:
        """Logout broker session."""
        raise NotImplementedError

    @abstractmethod
    def is_connected(self) -> bool:
        """Return True if broker is connected."""
        raise NotImplementedError

    @abstractmethod
    def subscribe_market_data(self) -> None:
        """Subscribe to live market feed."""
        raise NotImplementedError

    @abstractmethod
    def subscribe_orders(self) -> None:
        """Subscribe to order updates."""
        raise NotImplementedError

    @abstractmethod
    def subscribe_trades(self) -> None:
        """Subscribe to trade updates."""
        raise NotImplementedError

    @abstractmethod
    def subscribe_positions(self) -> None:
        """Subscribe to live positions."""
        raise NotImplementedError

    @abstractmethod
    def get_limits(self):
        """Fetch account limits."""
        raise NotImplementedError

    @abstractmethod
    def get_profile(self):
        """Fetch user profile."""
        raise NotImplementedError

"""
AEGIS

Broker Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class IBrokerAdapter(ABC):
    """
    Common broker interface implemented by every broker.
    """

    # =====================================================
    # Connection
    # =====================================================

    @abstractmethod
    def connect(self) -> bool:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def is_connected(self) -> bool:
        ...

    # =====================================================
    # Authentication
    # =====================================================

    @abstractmethod
    def login(self) -> bool:
        ...

    @abstractmethod
    def logout(self) -> None:
        ...

    # =====================================================
    # Account
    # =====================================================

    @abstractmethod
    def get_profile(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_limits(self) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_holdings(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_positions(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_orders(self) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_tradebook(self) -> list[dict[str, Any]]:
        ...

    # =====================================================
    # Order Management
    # =====================================================

    @abstractmethod
    def place_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def modify_order(
        self,
        **values: Any,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def cancel_order(
        self,
        orderno: str,
    ) -> dict[str, Any]:
        ...

    # =====================================================
    # Market Data
    # =====================================================

    @abstractmethod
    def subscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:
        ...

    @abstractmethod
    def unsubscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:
        ...

    @abstractmethod
    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_quote(
        self,
        exchange: str,
        token: str,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_option_chain(
        self,
        exchange: str,
        symbol: str,
        strike: str,
        count: int,
    ) -> dict[str, Any]:
        ...

    @abstractmethod
    def get_historical_data(
        self,
        **values: Any,
    ) -> list[dict[str, Any]]:
        ...

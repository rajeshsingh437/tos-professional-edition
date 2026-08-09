"""
AEGIS

Generic Broker Adapter

This layer provides a unified interface between BrokerManager and
individual broker implementations (Flattrade, GO, etc.).

BrokerManager never communicates directly with a broker.
"""

from __future__ import annotations

from typing import Any

from brokers.base.broker_interface import BrokerInterface
from brokers.manager import BrokerManager


class BrokerAdapter:
    """
    Generic broker façade.

    Delegates every broker operation to the active broker managed by
    BrokerManager.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        manager: BrokerManager | None = None,
    ) -> None:

        self.manager = manager or BrokerManager()

    @property
    def broker(self) -> BrokerInterface:
        """
        Return the currently active broker.
        """

        return self.manager.active_broker

    @property
    def broker_name(self) -> str:
        """
        Return the active broker name.
        """

        return self.manager.active_broker_name

    # ==========================================================
    # Authentication
    # ==========================================================

    @property
    def is_authenticated(self) -> bool:
        """
        Return authentication state of the active broker.
        """

        return self.broker.is_authenticated

    def login(self) -> bool:
        """
        Login using the active broker.
        """

        return self.broker.login()

    def logout(self) -> None:
        """
        Logout from the active broker.
        """

        self.broker.logout()

    # ==========================================================
    # Account
    # ==========================================================

    def profile(self) -> dict[str, Any]:
        """
        Return account profile.
        """

        return self.broker.get_profile()

    def funds(self) -> dict[str, Any]:
        """
        Return available funds.
        """

        return self.broker.get_funds()

    def limits(self) -> dict[str, Any]:
        """
        Return account limits.
        """

        return self.broker.get_limits()

    def holdings(self) -> list[dict[str, Any]]:
        """
        Return holdings.
        """

        return self.broker.get_holdings()

    def positions(self) -> list[dict[str, Any]]:
        """
        Return open positions.
        """

        return self.broker.get_positions()

    def orders(self) -> list[dict[str, Any]]:
        """
        Return order book.
        """

        return self.broker.get_orders()

    def trades(self) -> list[dict[str, Any]]:
        """
        Return trade book.
        """

        return self.broker.get_trades()

    def tradebook(self) -> list[dict[str, Any]]:
        """
        Return trade book (compatibility alias).
        """

        return self.broker.get_tradebook()

    # ==========================================================
    # Order Management
    # ==========================================================

    def place_order(
        self,
        *,
        exchange: str,
        symbol: str,
        quantity: int,
        order_type: str,
        transaction_type: str,
        product: str,
        price: float | None = None,
        trigger_price: float | None = None,
        validity: str = "DAY",
    ) -> dict[str, Any]:
        """
        Place order.
        """

        return self.broker.place_order(
            exchange=exchange,
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            transaction_type=transaction_type,
            product=product,
            price=price,
            trigger_price=trigger_price,
            validity=validity,
        )

    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Modify existing order.
        """

        return self.broker.modify_order(
            order_id,
            **kwargs,
        )

    def cancel_order(
        self,
        order_id: str,
    ) -> dict[str, Any]:
        """
        Cancel order.
        """

        return self.broker.cancel_order(order_id)

    # ==========================================================
    # Market Data
    # ==========================================================

    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        """
        Search broker symbols.
        """

        return self.broker.search_symbol(text)

    def quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Return live quote.
        """

        return self.broker.get_quote(
            exchange,
            symbol,
        )

    def option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:
        """
        Return option chain.
        """

        return self.broker.get_option_chain(
            symbol,
            expiry,
        )

    def historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> list[dict[str, Any]]:
        """
        Return historical candles.
        """

        return self.broker.get_historical_data(
            exchange,
            symbol,
            interval,
            start,
            end,
        )
    # ==========================================================
    # Information
    # ==========================================================

    @property
    def version(self) -> str:
        """
        Return active broker adapter version.
        """

        return self.broker.broker_version



    @property
    def available_brokers(self) -> list[str]:
        """
        Return registered brokers.
        """

        return self.manager.available_brokers()

    def use(self, broker: str) -> None:
        """
        Reserved for future multi-broker support.
        """

        raise NotImplementedError(
            "Multiple brokers are not implemented yet."
        )

    # ==========================================================
    # Context Manager
    # ==========================================================

    def __enter__(self):
        """
        Automatically login.

        Example:

            with BrokerAdapter() as broker:
                ...
        """

        self.login()

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):
        """
        Automatically logout.
        """

        self.logout()

        return False

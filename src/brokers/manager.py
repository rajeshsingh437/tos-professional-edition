"""
AEGIS Trading Platform

Module:
Broker Manager

Purpose:
Single orchestration layer between the application and supported brokers.

The BrokerManager owns broker registration, broker selection, lifecycle
management and delegates broker operations to the active broker adapter.

Version:
1.0.0

Status:
Production

Architecture:
Broker Gateway

Author:
AEGIS Project
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from brokers.base.broker_interface import BrokerInterface
from brokers.flattrade.adapter import FlattradeBroker


# ============================================================
# Exceptions
# ============================================================


class BrokerError(RuntimeError):
    """
    Generic broker exception exposed to the rest of AEGIS.

    Broker-specific exceptions should not escape BrokerManager.
    """


# ============================================================
# Status Model
# ============================================================


@dataclass(slots=True)
class BrokerStatus:
    """
    Unified broker status returned to the UI.
    """

    broker: str

    connected: bool

    authenticated: bool

    relay: bool

    rest: bool

    websocket: bool

    version: str


# ============================================================
# Broker Manager
# ============================================================


class BrokerManager:
    """
    Broker Gateway for AEGIS.

    Responsibilities
    ----------------

    • Register available brokers

    • Maintain active broker

    • Delegate broker operations

    • Present one consistent API to the application

    The BrokerManager intentionally contains no broker-specific business
    logic. Every broker implementation lives inside its own adapter.
    """

    VERSION = "1.0.0"

    DEFAULT_BROKER = "flattrade"

    def __init__(
        self,
        brokers: dict[str, BrokerInterface] | None = None,
        active_broker: str | None = None,
    ) -> None:
        """
        Initialize the Broker Gateway.

        Parameters
        ----------
        brokers
            Optional dependency injection for testing.

        active_broker
            Name of the active broker.
        """

        self._brokers = brokers or {
            "flattrade": FlattradeBroker(),
        }

        self._active_name = (
            active_broker
            or self.DEFAULT_BROKER
        )

        if self._active_name not in self._brokers:
            raise BrokerError(
                f"Unknown broker '{self._active_name}'."
            )

        self._active = self._brokers[self._active_name]

    # ============================================================
    # Properties
    # ============================================================

    @property
    def active_broker(self) -> BrokerInterface:
        """
        Return the currently active broker adapter.
        """
        return self._active

    @property
    def active_broker_name(self) -> str:
        """
        Return the active broker name.
        """
        return self._active_name

    # ============================================================
    # Authentication
    # ============================================================

    @property
    def is_authenticated(self) -> bool:
        """
        Return authentication state.
        """
        return self._active.is_authenticated

    def login(self) -> bool:
        """
        Authenticate the active broker.
        """
        try:
            return self._active.login()

        except Exception as error:
            raise BrokerError(
                f"Broker login failed: {error}"
            ) from error

    def logout(self) -> None:
        """
        Logout from the active broker.
        """
        try:
            self._active.logout()

        except Exception as error:
            raise BrokerError(
                f"Broker logout failed: {error}"
            ) from error

    # ============================================================
    # Status
    # ============================================================

    def status(self) -> BrokerStatus:
        """
        Return unified broker status.

        Relay/REST/WebSocket health will become live values in
        subsequent Broker Gateway versions.
        """

        return BrokerStatus(
            broker=self._active_name,
            connected=True,
            authenticated=self.is_authenticated,
            relay=True,
            rest=True,
            websocket=False,
            version=self.VERSION,
        )

    # ============================================================
    # Account
    # ============================================================

    def funds(self) -> dict[str, Any]:
        """
        Return broker funds.
        """
        try:
            return self._active.get_funds()

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve funds: {error}"
            ) from error

    def positions(self) -> list[dict[str, Any]]:
        """
        Return broker positions.
        """
        try:
            return self._active.get_positions()

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve positions: {error}"
            ) from error

    def orders(self) -> list[dict[str, Any]]:
        """
        Return broker orders.
        """
        try:
            return self._active.get_orders()

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve orders: {error}"
            ) from error

    def holdings(self) -> list[dict[str, Any]]:
        """
        Return broker holdings.
        """
        try:
            return self._active.get_holdings()

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve holdings: {error}"
            ) from error

    def trades(self) -> list[dict[str, Any]]:
        """
        Return broker tradebook.
        """
        try:
            return self._active.get_trades()

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve trades: {error}"
            ) from error

    # ============================================================
    # Order Management
    # ============================================================

    def place_order(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Place an order.
        """
        try:
            return self._active.place_order(
                **kwargs,
            )

        except Exception as error:
            raise BrokerError(
                f"Order placement failed: {error}"
            ) from error

    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Modify an order.
        """
        try:
            return self._active.modify_order(
                order_id,
                **kwargs,
            )

        except Exception as error:
            raise BrokerError(
                f"Order modification failed: {error}"
            ) from error

    def cancel_order(
        self,
        order_id: str,
    ) -> dict[str, Any]:
        """
        Cancel an order.
        """
        try:
            return self._active.cancel_order(
                order_id,
            )

        except Exception as error:
            raise BrokerError(
                f"Order cancellation failed: {error}"
            ) from error

    # ============================================================
    # Market Data
    # ============================================================

    def quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:
        """
        Return a live quote.
        """
        try:
            return self._active.get_quote(
                exchange,
                symbol,
            )

        except Exception as error:
            raise BrokerError(
                f"Unable to retrieve quote: {error}"
            ) from error

    def search(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        """
        Search broker instruments.
        """
        try:
            return self._active.search_symbol(
                text,
            )

        except Exception as error:
            raise BrokerError(
                f"Instrument search failed: {error}"
            ) from error

    def option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:
        """
        Return option chain.
        """
        try:
            return self._active.get_option_chain(
                symbol,
                expiry,
            )

        except Exception as error:
            raise BrokerError(
                f"Option chain failed: {error}"
            ) from error

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
        try:
            return self._active.get_historical_data(
                exchange,
                symbol,
                interval,
                start,
                end,
            )

        except Exception as error:
            raise BrokerError(
                f"Historical data request failed: {error}"
            ) from error

    # ============================================================
    # Broker Management
    # ============================================================

    def register(
        self,
        name: str,
        broker: BrokerInterface,
    ) -> None:
        """
        Register a broker implementation.

        Future brokers (GO, Zerodha, etc.) can be added without
        modifying BrokerManager itself.
        """

        self._brokers[name] = broker

    def switch(
        self,
        broker_name: str,
    ) -> None:
        """
        Switch the active broker.

        Existing authenticated sessions remain untouched.
        """

        if broker_name not in self._brokers:
            raise BrokerError(
                f"Unknown broker '{broker_name}'."
            )

        self._active_name = broker_name
        self._active = self._brokers[broker_name]

    def activate(
        self,
        broker_name: str,
    ) -> None:
        """
        Activate a broker by name.

        Compatibility wrapper for BrokerAdapter.
        """
        self.switch(broker_name)

    def select(
        self,
        broker_name: str,
    ) -> None:
        """
        Switch active broker.

        Compatibility wrapper for BrokerAdapter.
        """
        self.activate(broker_name)

    def available_brokers(self) -> list[str]:
        """
        Return registered brokers.
        """

        return sorted(
            self._brokers.keys()
        )

    def broker(
        self,
        name: str,
    ) -> BrokerInterface:
        """
        Return a broker instance without making it active.
        """

        try:
            return self._brokers[name]

        except KeyError as error:
            raise BrokerError(
                f"Unknown broker '{name}'."
            ) from error

    # ============================================================
    # Future Hooks
    # ============================================================

    def shutdown(self) -> None:
        """
        Clean shutdown for all registered brokers.

        Future versions will disconnect WebSockets, stop
        background workers and close network sessions.
        """

        pass


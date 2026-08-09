"""
AEGIS Professional Edition
==========================

Broker Interface

Every broker (Flattrade, Zerodha, Dhan, AngelOne, etc.)
must implement this interface.

The rest of AEGIS NEVER communicates directly with
broker-specific code.

Modules such as:

    • Journal
    • Automation Engine
    • Screenshot Engine
    • Risk Manager
    • Kill Switch
    • Analytics

must only communicate through BrokerInterface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from typing import Any
from typing import Dict
from typing import List
from typing import Optional


class BrokerInterface(ABC):
    """
    Generic broker contract.

    Every supported broker MUST implement every method
    defined below.

    This allows AEGIS to remain completely broker
    independent.
    """

    # =====================================================
    # Authentication
    # =====================================================

    @abstractmethod
    def login(self) -> bool:
        """
        Authenticate broker session.

        Returns
        -------
        bool
            True when authentication succeeds.
        """
        raise NotImplementedError

    @abstractmethod
    def logout(self) -> None:
        """
        Logout broker session.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def is_authenticated(self) -> bool:
        """
        Returns current authentication state.
        """
        raise NotImplementedError

    # =====================================================
    # Account
    # =====================================================

    @abstractmethod
    def get_profile(self) -> Dict[str, Any]:
        """
        Returns broker profile.
        """
        raise NotImplementedError

    @abstractmethod
    def get_funds(self) -> Dict[str, Any]:
        """
        Returns account funds / limits.
        """
        raise NotImplementedError

    @abstractmethod
    def get_limits(
        self,
    ) -> Dict[str, Any]:
        """
        Returns account limits / margin.

        Default implementation for brokers that expose
        limits separately from funds.
        """
        raise NotImplementedError

    @abstractmethod
    def get_holdings(self) -> List[Dict[str, Any]]:
        """
        Returns holdings.
        """
        raise NotImplementedError

    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Returns current positions.
        """
        raise NotImplementedError

    @abstractmethod
    def get_orders(self) -> List[Dict[str, Any]]:
        """
        Returns order book.
        """
        raise NotImplementedError

    @abstractmethod
    def get_trades(self) -> List[Dict[str, Any]]:
        """
        Returns trade book.
        """
        raise NotImplementedError

    @abstractmethod
    def get_tradebook(
        self,
    ) -> List[Dict[str, Any]]:
        """
        Compatibility alias.

        Some broker APIs expose TradeBook while
        others expose Trades.

        AEGIS supports both.
        """
        raise NotImplementedError

    # =====================================================
    # Order Management
    # =====================================================

    @abstractmethod
    def place_order(
        self,
        *,
        exchange: str,
        symbol: str,
        quantity: int,
        order_type: str,
        transaction_type: str,
        product: str,
        price: Optional[float] = None,
        trigger_price: Optional[float] = None,
        validity: str = "DAY",
    ) -> Dict[str, Any]:
        """
        Place new order.
        """
        raise NotImplementedError

    @abstractmethod
    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Modify existing order.
        """
        raise NotImplementedError

    @abstractmethod
    def cancel_order(
        self,
        order_id: str,
    ) -> Dict[str, Any]:
        """
        Cancel existing order.
        """
        raise NotImplementedError

    # =====================================================
    # Market Data
    # =====================================================

    @abstractmethod
    def search_symbol(
        self,
        text: str,
    ) -> List[Dict[str, Any]]:
        """
        Search broker symbols.
        """
        raise NotImplementedError

    @abstractmethod
    def get_quote(
        self,
        exchange: str,
        symbol: str,
    ) -> Dict[str, Any]:
        """
        Returns current market quote.
        """
        raise NotImplementedError

    @abstractmethod
    def get_option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> Dict[str, Any]:
        """
        Returns option chain.
        """
        raise NotImplementedError

    @abstractmethod
    def get_historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> List[Dict[str, Any]]:
        """
        Historical OHLC.
        """
        raise NotImplementedError
        # =====================================================
    # WebSocket
    # =====================================================

    @abstractmethod
    def connect_market_data(self) -> None:
        """
        Start market data stream.
        """
        raise NotImplementedError

    @abstractmethod
    def disconnect_market_data(self) -> None:
        """
        Stop market data stream.
        """
        raise NotImplementedError

    @abstractmethod
    def subscribe(
        self,
        instruments: List[str],
    ) -> None:
        """
        Subscribe to market feed.
        """
        raise NotImplementedError

    @abstractmethod
    def unsubscribe(
        self,
        instruments: List[str],
    ) -> None:
        """
        Unsubscribe from market feed.
        """
        raise NotImplementedError

    # =====================================================
    # Event Callbacks
    # =====================================================

    @abstractmethod
    def on_tick(
        self,
        callback,
    ) -> None:
        """
        Register tick callback.
        """
        raise NotImplementedError

    @abstractmethod
    def on_order_update(
        self,
        callback,
    ) -> None:
        """
        Register order update callback.
        """
        raise NotImplementedError

    @abstractmethod
    def on_trade(
        self,
        callback,
    ) -> None:
        """
        Register trade callback.
        """
        raise NotImplementedError

    @abstractmethod
    def on_position_update(
        self,
        callback,
    ) -> None:
        """
        Register position callback.
        """
        raise NotImplementedError

    @abstractmethod
    def on_disconnect(
        self,
        callback,
    ) -> None:
        """
        Register disconnect callback.
        """
        raise NotImplementedError

    # =====================================================
    # Session
    # =====================================================

    @abstractmethod
    def refresh_session(self) -> bool:
        """
        Refresh broker session.
        """
        raise NotImplementedError

    @abstractmethod
    def heartbeat(self) -> bool:
        """
        Verify broker connectivity.

        Returns
        -------
        bool
            True when broker session is alive.
        """
        raise NotImplementedError

    # =====================================================
    # Information
    # =====================================================

    @property
    @abstractmethod
    def broker_name(self) -> str:
        """
        Broker display name.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def broker_version(self) -> str:
        """
        Broker adapter version.
        """
        raise NotImplementedError

    # =====================================================
    # Context Manager
    # =====================================================

    def __enter__(self):
        """
        Allow:

            with BrokerAdapter() as broker:
                ...
        """
        self.login()
        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        """
        Automatically logout.
        """
        self.logout()

        return False


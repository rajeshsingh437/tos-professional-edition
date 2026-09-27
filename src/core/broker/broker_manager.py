"""
AEGIS

Broker Manager

Single entry point for all broker operations.
"""

from __future__ import annotations

from src.core.broker.adapters.flattrade_adapter import (
    FlattradeAdapter,
)
from src.core.events.event_bus import EventBus
from src.core.market.market_data_service import MarketDataService


class BrokerManager:
    """
    Coordinates the active broker adapter.
    """

    def __init__(self) -> None:

        self.event_bus = EventBus()

        self.adapter = FlattradeAdapter(
            event_bus=self.event_bus
        )

        self.market_data = MarketDataService(
            event_bus=self.event_bus
        )

    # ==========================================================
    # Market Data Service
    # ==========================================================

    def get_latest_tick(self, exchange: str, token: str):
        return self.market_data.get_latest(exchange, token)

    def get_all_latest_ticks(self):
        return self.market_data.get_all_latest()

    def market_data_snapshot(self):
        return self.market_data.snapshot()

    # ==========================================================
    # Lifecycle
    # ==========================================================

    def start(self) -> None:
        """
        Initialize broker services.
        """

        self.adapter.connect()

    def login(self) -> bool:
        """
        Authenticate with broker.
        """

        return self.adapter.login()

    def logout(self) -> None:
        """
        Logout from broker.
        """

        self.adapter.logout()

    def connect(self) -> bool:
        """
        Connect broker.
        """

        return self.adapter.connect()

    def disconnect(self) -> None:
        """
        Disconnect broker.
        """

        self.adapter.disconnect()

    # ==========================================================
    # Properties
    # ==========================================================

    @property
    def connected(self) -> bool:

        return self.adapter.is_connected()

    @property
    def authenticated(self) -> bool:

        return self.adapter.auth.is_authenticated

    # ==========================================================
    # Account
    # ==========================================================

    def get_profile(self):

        return self.adapter.get_profile()

    def get_limits(self):

        return self.adapter.get_limits()

    def get_holdings(self):

        return self.adapter.get_holdings()

    def get_positions(self):

        return self.adapter.get_positions()

    def get_orders(self):

        return self.adapter.get_orders()

    def get_tradebook(self):

        return self.adapter.get_tradebook()

    # ==========================================================
    # Orders
    # ==========================================================

    def place_order(self, **kwargs):

        return self.adapter.place_order(**kwargs)

    def modify_order(self, order_id, **kwargs):

        return self.adapter.modify_order(
            order_id,
            **kwargs,
        )

    def cancel_order(self, order_id):

        return self.adapter.cancel_order(
            order_id
        )

    # ==========================================================
    # Market Data
    # ==========================================================

    def search_symbol(self, text, exchange='NSE'):

        return self.adapter.search_symbol(
            text,
            exchange=exchange,
        )

    def get_quote(
        self,
        exchange,
        token,
    ):

        return self.adapter.get_quote(
            exchange,
            token,
        )

    def get_time_price_series(
        self,
        exchange,
        token,
        start_time,
        interval,
    ):

        return self.adapter.get_time_price_series(
            exchange,
            token,
            start_time,
            interval,
        )

    def subscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:

        self.adapter.subscribe_market_data(
            symbols
        )

    def unsubscribe_market_data(
        self,
        symbols,
    ):

        self.adapter.unsubscribe_market_data(
            symbols
        )

    def subscribe_orders(self):

        self.adapter.subscribe_orders()

    def subscribe_trades(self):

        self.adapter.subscribe_trades()

    def subscribe_positions(self):

        self.adapter.subscribe_positions()





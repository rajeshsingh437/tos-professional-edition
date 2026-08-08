"""
AEGIS

Flattrade Broker Adapter

Concrete implementation of the broker interface.
"""
from __future__ import annotations

import time
import webbrowser

from typing import Any, Optional

from ..broker_interface import IBrokerAdapter

from ..services.auth_manager import (
    AuthenticationManager,
)

from ..services.oauth_client import (
    OAuthClient,
)
from ..services.relay_client import (
    RelayClient,
)

from ..services.rest_client import (
    RestClient,
)
from ..services.oauth_server import (
    OAuthServer,
)



class FlattradeAdapter(IBrokerAdapter):
    """
    Flattrade broker implementation.
    """

    def __init__(self) -> None:

        self._connected = False
        self._authenticated = False

        self.auth = AuthenticationManager()

        self.oauth = OAuthClient(
            api_key=self.auth.broker["api_key"],
            api_secret=self.auth.broker["api_secret"],
        )
        self.oauth_server = OAuthServer()

        self.relay = RelayClient(
            relay_url=self.auth.broker["relay_url"],
            shared_secret=self.auth.broker["relay_shared_secret"],
        )

        self.rest: Optional[RestClient] = None

    # =====================================================
    # Connection
    # =====================================================

    def connect(self) -> bool:

        print("Connecting to Flattrade...")

        self._connected = True

        return True

    def disconnect(self) -> None:

        print("Disconnected.")

        self._connected = False
        self._authenticated = False

    def is_connected(self) -> bool:

        return self._connected

    # =====================================================
    # Authentication
    # =====================================================

    def login(self) -> bool:

        print("Authenticating with Flattrade...")

        # Already logged in
        if self.auth.is_authenticated:

            self._authenticated = True

            self.rest = RestClient(
                access_token=self.auth.state.access_token,
                client_id=self.auth.broker["api_key"],
            )

            return True

        # Start callback server
        print("Starting OAuth callback server...")
        self.oauth_server.start()
        while not self.oauth_server.ready:
            time.sleep(0.1)

        try:
            # Open browser
            print("Opening browser...")
            webbrowser.open(self.oauth.authorization_url)
            print("Browser opened")

            print("Waiting for login...")

            while self.oauth_server.request_code is None:
                time.sleep(0.25)

            request_code = self.oauth_server.request_code

            print("Received request code.")

            payload = self.relay.complete_login(request_code)

            access_token = payload["token"]

            self.auth.save_authenticated_session(
                access_token=access_token,
            )

            self.rest = RestClient(
                access_token=access_token,
                client_id=self.auth.broker["api_key"],
            )

            self._authenticated = True

            print("Authentication successful.")

         #   self.oauth_server.stop_server()

            return True
        finally:
            pass
          #  self.oauth_server.stop_server()

    def logout(self) -> None:

        self.auth.clear()

        self._authenticated = False

    def refresh_session(self) -> bool:

        return self.auth.is_authenticated

    def heartbeat(self) -> bool:

        return self._connected
    # =====================================================
    # Account
    # =====================================================

    def get_profile(self) -> dict[str, Any]:

        return {
            "broker": "Flattrade",
            "connected": self._connected,
            "authenticated": self._authenticated,
        }

    def get_limits(self) -> dict[str, Any]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_limits()

    def get_holdings(self) -> list[dict[str, Any]]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_holdings()

    def get_positions(self) -> list[dict[str, Any]]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_positions()

    def get_orders(self) -> list[dict[str, Any]]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_orders()

    def get_tradebook(self) -> list[dict[str, Any]]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_tradebook()

    # =====================================================
    # Order Management
    # =====================================================

    def place_order(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.place_order(**kwargs)

    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.modify_order(
            norenordno=order_id,
            **kwargs,
        )

    def cancel_order(
        self,
        order_id: str,
    ) -> dict[str, Any]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.cancel_order(order_id)
       # =====================================================
    # Market Data
    # =====================================================

    def subscribe_market_data(self) -> None:

        print("Market data subscription.")

    def unsubscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:
        """
        Unsubscribe live market data.
        """

        print(f"Unsubscribing market data: {symbols}")

    def subscribe_orders(self) -> None:

        print("Order subscription.")

    def subscribe_trades(self) -> None:

        print("Trade subscription.")

    def subscribe_positions(self) -> None:

        print("Position subscription.")

    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.search_symbol(text)

    def get_quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:
        if self.rest is None:
            raise RuntimeError("Broker is not authenticated.")

        return self.rest.get_quote(
            exchange,
            symbol,
        )

    def get_option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:

        raise NotImplementedError(
            "Option Chain API migration pending."
        )

    def get_historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> list[dict[str, Any]]:

        raise NotImplementedError(
            "Historical Data API migration pending."
        )

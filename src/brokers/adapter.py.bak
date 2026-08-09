"""Flattrade broker adapter for AEGIS."""

from __future__ import annotations

import time
import webbrowser
from typing import Any, Callable

from brokers.base.broker_interface import BrokerInterface
from brokers.flattrade.auth_manager import AuthenticationManager
from brokers.flattrade.oauth_client import OAuthClient, OAuthError
from brokers.flattrade.oauth_server import OAuthServer
from brokers.flattrade.rest import RestClient


OAUTH_CALLBACK_TIMEOUT_SECONDS = 180
OAUTH_CALLBACK_POLL_SECONDS = 0.25
ADAPTER_VERSION = "1.0.0"


class FlattradeAdapter(BrokerInterface):
    """Concrete Flattrade implementation of the AEGIS broker contract."""

    def __init__(self) -> None:
        """Initialize authentication, OAuth callback server and REST client."""

        self.auth = AuthenticationManager()

        self.oauth = OAuthClient(
            api_key=self.auth.broker["api_key"],
            api_secret=self.auth.broker["api_secret"],
        )

        self.oauth_server = OAuthServer()
        self._oauth_server_started = False

        self.rest = RestClient(
            access_token=self.auth.state.access_token,
            client_id=self.auth.state.client_id,
        )

    # ==========================================================
    # Authentication
    # ==========================================================

    @property
    def is_authenticated(self) -> bool:
        """Return current authentication state."""

        return self.auth.is_authenticated

    def login(self) -> bool:
        """Authenticate using the Flattrade OAuth flow via the Oracle Cloud relay."""

        if self.is_authenticated:
            print("Already authenticated.")
            return True

        self.oauth_server.request_code = None

        if not self._oauth_server_started:
            print("Starting OAuth callback server...")
            self.oauth_server.start()
            self._oauth_server_started = True

        print("Opening Flattrade login page...")
        webbrowser.open(self.oauth.authorization_url)

        request_code = self._wait_for_request_code()

        print("Request code received. Forwarding to Oracle Cloud relay...")

        import os
        import requests

        relay_secret = os.getenv("RELAY_SHARED_SECRET", "YOUR_SECRET_HERE")

        relay_response = requests.post(
            "http://localhost:8091/complete_login",
            json={"code": request_code},
            headers={"Authorization": f"Bearer {relay_secret}"},
            timeout=15,
        )

        if relay_response.status_code != 200:
            raise OAuthError(f"Relay login failed: {relay_response.text}")

        token_response = relay_response.json()

        access_token = str(token_response.get("token") or token_response.get("access_token", ""))
        client_id = str(token_response.get("client_id") or token_response.get("client", ""))

        self.auth.save_authenticated_session(
            access_token=access_token,
            client_id=client_id,
        )

        self.rest.access_token = access_token
        self.rest.client_id = client_id

        print("Authentication successful.")

        return True

    def _wait_for_request_code(self) -> str:
        """Wait for the OAuth callback to return the request code."""

        deadline = (
            time.monotonic()
            + OAUTH_CALLBACK_TIMEOUT_SECONDS
        )

        while time.monotonic() < deadline:

            request_code = self.oauth_server.request_code

            if request_code:
                return request_code

            time.sleep(
                OAUTH_CALLBACK_POLL_SECONDS
            )

        raise OAuthError(
            "Timed out waiting for Flattrade OAuth callback."
        )

    # ==========================================================
    # Account
    # ==========================================================

    def logout(self) -> None:
        """Clear the locally saved authentication session."""

        self.auth.clear()

        self.rest.access_token = ""
        self.rest.client_id = ""

    def get_profile(self) -> dict[str, Any]:
        """Fetch the account profile when implemented."""

        raise NotImplementedError(
            "Flattrade profile retrieval is not implemented."
        )

    def get_funds(self) -> dict[str, Any]:
        """Return available funds."""

        return self.get_limits()

    def get_limits(self) -> dict[str, Any]:
        """Return account limits."""

        return self.rest.get_limits()

    def get_holdings(self) -> list[dict[str, Any]]:
        """Return holdings."""

        return self.rest.get_holdings()

    def get_positions(self) -> list[dict[str, Any]]:
        """Return open positions."""

        return self.rest.get_positions()

    def get_orders(self) -> list[dict[str, Any]]:
        """Return order book."""

        return self.rest.get_orders()

    def get_trades(self) -> list[dict[str, Any]]:
        """Return trade book."""

        return self.rest.get_tradebook()

    def get_tradebook(self) -> list[dict[str, Any]]:
        """Return trade book."""

        return self.rest.get_tradebook()

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
        """Place a new order."""

        payload: dict[str, Any] = {
            "exch": exchange,
            "tsym": symbol,
            "qty": str(quantity),
            "trantype": transaction_type,
            "prctyp": order_type,
            "prd": product,
            "ret": validity,
        }

        if price is not None:
            payload["prc"] = str(price)

        if trigger_price is not None:
            payload["trgprc"] = str(trigger_price)

        return self.rest.place_order(
            **payload,
        )

    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Modify an existing order."""

        payload = {
            "norenordno": order_id,
            **kwargs,
        }

        return self.rest.modify_order(
            **payload,
        )

    def cancel_order(
        self,
        order_id: str,
    ) -> dict[str, Any]:
        """Cancel an existing order."""

        return self.rest.cancel_order(
            orderno=order_id,
        )

    # ==========================================================
    # Market Data
    # ==========================================================

    def search_symbol(
        self,
        text: str,
    ) -> list[dict[str, Any]]:
        """Search broker symbols."""

        return self.rest.search_symbol(
            text=text,
        )

    def get_quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:
        """Return current market quote."""

        return self.rest.get_quote(
            exchange=exchange,
            symbol=symbol,
        )

    def get_option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:
        """Return option chain."""

        return self.rest.get_option_chain(
            symbol=symbol,
            expiry=expiry,
        )

    def get_historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> list[dict[str, Any]]:
        """Return historical data."""

        return self.rest.get_historical_data(
            exchange=exchange,
            symbol=symbol,
            interval=interval,
            start=start,
            end=end,
        )

    # ==========================================================
    # WebSocket
    # ==========================================================

    def connect_market_data(self) -> None:
        """Connect to the market data stream."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def disconnect_market_data(self) -> None:
        """Disconnect the market data stream."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def subscribe(
        self,
        instruments: list[str],
    ) -> None:
        """Subscribe to market data."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def unsubscribe(
        self,
        instruments: list[str],
    ) -> None:
        """Unsubscribe from market data."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    # ==========================================================
    # Event Callbacks
    # ==========================================================

    def on_tick(
        self,
        callback: Callable[..., Any],
    ) -> None:
        """Register a tick callback."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def on_order_update(
        self,
        callback: Callable[..., Any],
    ) -> None:
        """Register an order update callback."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def on_trade(
        self,
        callback: Callable[..., Any],
    ) -> None:
        """Register a trade callback."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def on_position_update(
        self,
        callback: Callable[..., Any],
    ) -> None:
        """Register a position callback."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    def on_disconnect(
        self,
        callback: Callable[..., Any],
    ) -> None:
        """Register a disconnect callback."""

        raise NotImplementedError(
            "Flattrade WebSocket support is not implemented."
        )

    # ==========================================================
    # Session
    # ==========================================================

    def refresh_session(self) -> bool:
        """Return whether a valid session is available."""

        return self.is_authenticated

    def heartbeat(self) -> bool:
        """Return broker connection status."""

        return self.is_authenticated

    # ==========================================================
    # Information
    # ==========================================================

    @property
    def broker_name(self) -> str:
        """Return broker name."""

        return "Flattrade"

    @property
    def broker_version(self) -> str:
        """Return adapter version."""

        return ADAPTER_VERSION

    # ==========================================================
    # Context Manager
    # ==========================================================

    def __enter__(self) -> "FlattradeAdapter":
        """Enter context manager."""

        self.login()

        return self

    def __exit__(
        self,
        exc_type: object,
        exc_val: object,
        exc_tb: object,
    ) -> bool:
        """Exit context manager."""

        self.logout()

        return False

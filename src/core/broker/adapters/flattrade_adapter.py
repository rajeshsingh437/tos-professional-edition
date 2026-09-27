"""
AEGIS

Flattrade Broker Adapter

Concrete implementation of the broker interface.
"""

from __future__ import annotations

import time
import webbrowser

from datetime import datetime, timezone
from typing import Any, Optional

from zoneinfo import ZoneInfo

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

from ..services.websocket_manager import (
    WebSocketManager,
)

from ..services.oauth_server import (
    OAuthServer,
)

from ...events.event_bus import EventBus
from ...events.tick_normalizer import TickNormalizer


class FlattradeAdapter(IBrokerAdapter):
    """
    Flattrade broker implementation.
    """

    def __init__(self, event_bus: EventBus | None = None) -> None:

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
            shared_secret=self.auth.broker[
                "relay_shared_secret"
            ],
        )

        self.rest: Optional[RestClient] = None
        self.websocket: Optional[WebSocketManager] = None

        # =====================================================
        # Canonical Market Data
        # =====================================================

        self.event_bus = event_bus if event_bus is not None else EventBus()
        self.tick_normalizer = TickNormalizer()

        # =====================================================
        # Market Data
        # =====================================================

        self._ist = ZoneInfo("Asia/Kolkata")
    # =====================================================
    # WebSocket Tick Callback
    # =====================================================

    def _handle_tick(
        self,
        tick: dict[str, Any],
    ) -> None:
        """
        Receive a raw Flattrade WebSocket payload.

        The broker payload is normalized into the canonical
        AEGIS MarketTick model and published through EventBus.
        """

        try:
            market_tick = self.tick_normalizer.normalize(
                tick
            )

            self.event_bus.publish(
                market_tick.event_type,
                market_tick,
            )

            print(
                "CANONICAL MARKET TICK:",
                market_tick,
            )

        except Exception as exc:
            print(
                f"Market tick normalization failed: {exc}"
            )

    # =====================================================
    # Connection
    # =====================================================

    def connect(self) -> bool:

        print('Connecting to Flattrade...')

        result = self.login()

        self._connected = bool(result)

        return self._connected

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

        # ==================================================
        # Existing Saved Session
        # ==================================================

        if self.auth.is_authenticated:

            access_token = self.auth.state.access_token
            client_id = self.auth.state.client_id

            if not access_token or not client_id:

                self.auth.clear()

            else:

                self.rest = RestClient(
                    access_token=access_token,
                    client_id=client_id,
                )

                try:

                    # Verify the saved REST session first.
                    self.rest.get_limits()

                    self._authenticated = True

                    print(
                        "Existing session restored."
                    )

                    # Start realtime WebSocket.
                    self._start_websocket(
                        access_token=access_token,
                        client_id=client_id,
                    )

                    return True

                except Exception as exc:

                    print(
                        "Saved session has expired."
                    )

                    print(
                        f"Session verification failed: {exc}"
                    )

                    print(
                        "Starting fresh login..."
                    )

                    self.auth.clear()

                    self.rest = None
                    self.websocket = None

        # ==================================================
        # Start OAuth Callback Server
        # ==================================================

        print(
            "Starting OAuth callback server..."
        )

        self.oauth_server.start()

        while not self.oauth_server.ready:

            time.sleep(0.1)

        try:

            print("Opening browser...")

            webbrowser.open(
                self.oauth.authorization_url
            )

            print("Browser opened")

            print(
                "Waiting for login..."
            )

            while (
                self.oauth_server.request_code
                is None
            ):

                time.sleep(0.25)

            request_code = (
                self.oauth_server.request_code
            )

            print(
                "Received request code."
            )

            # ==================================================
            # Complete Login Through Relay
            # ==================================================

            payload = (
                self.relay.complete_login(
                    request_code
                )
            )

            print("RELAY RESPONSE PAYLOAD:", payload)
            access_token = str(payload.get("token") or payload.get("access_token") or "")
            client_id = str(
                payload.get("client")
                or payload.get("client_id")
                or self.auth.broker.get("client_id")
                or ""
            )

            # ==================================================
            # Save Session
            # ==================================================

            self.auth.save_authenticated_session(
                access_token=access_token,
                client_id=client_id,
            )

            # ==================================================
            # REST Client
            # ==================================================

            self.rest = RestClient(
                access_token=access_token,
                client_id=client_id,
            )

            # ==================================================
            # Authentication State
            # ==================================================

            self._authenticated = True

            print(
                "Authentication successful."
            )

            # ==================================================
            # WebSocket
            # ==================================================

            self._start_websocket(
                access_token=access_token,
                client_id=client_id,
            )

            return True

        finally:

            pass

            # Keep callback server behaviour unchanged
            # until the authentication flow is fully tested.
            #
            # self.oauth_server.stop_server()
                # =====================================================
    # WebSocket
    # =====================================================

    def _start_websocket(
        self,
        access_token: str,
        client_id: str,
    ) -> None:
        """
        Start the broker realtime WebSocket connection.
        """

        # Stop an existing websocket first.
        if self.websocket is not None:
            try:
                self.websocket.disconnect()
            except Exception:
                pass

        self.websocket = WebSocketManager(
            access_token=access_token,
            client_id=client_id,
            on_tick=self._handle_tick,
        )

        self.websocket.connect()

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

    def get_profile(
        self,
    ) -> dict[str, Any]:

        return {
            "broker": "Flattrade",
            "connected": self._connected,
            "authenticated": self._authenticated,
        }

    def get_limits(
        self,
    ) -> dict[str, Any]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_limits()

    def get_holdings(
        self,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_holdings()

    def get_positions(
        self,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_positions()

    def get_orders(
        self,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_orders()

    def get_tradebook(
        self,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_tradebook()

    # =====================================================
    # Order Management
    # =====================================================

    def place_order(
        self,
        **kwargs: Any,
    ) -> dict[str, Any]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.place_order(
            **kwargs
        )

    def modify_order(
        self,
        order_id: str,
        **kwargs: Any,
    ) -> dict[str, Any]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.modify_order(
            norenordno=order_id,
            **kwargs,
        )

    def cancel_order(
        self,
        order_id: str,
    ) -> dict[str, Any]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.cancel_order(
            order_id
        )

    # =====================================================
    # Market Data
    # =====================================================

    def subscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:
        """
        Subscribe to realtime market data through Flattrade WebSocket.
        """

        if self.websocket is None:
            raise RuntimeError(
                "WebSocket is not initialized."
            )

        self.websocket.subscribe(symbols)

    def unsubscribe_market_data(
        self,
        symbols: list[str],
    ) -> None:
        """
        Unsubscribe from realtime market data through Flattrade WebSocket.
        """

        if self.websocket is None:
            raise RuntimeError(
                "WebSocket is not initialized."
            )

        if hasattr(self.websocket, "unsubscribe"):
            self.websocket.unsubscribe(symbols)

        print(
            f"Unsubscribing market data: {symbols}"
        )

    def subscribe_orders(self) -> None:

        print("Order subscription.")

    def subscribe_trades(self) -> None:

        print("Trade subscription.")

    def subscribe_positions(self) -> None:

        print("Position subscription.")

    # =====================================================
    # Search Scrip
    # =====================================================

    def search_symbol(
        self,
        text: str,
        exchange: str = "NSE",
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.search_symbol(
            exchange=exchange,
            searchtext=text,
        )

    # =====================================================
    # Quote
    # =====================================================

    def get_quote(
        self,
        exchange: str,
        symbol: str,
    ) -> dict[str, Any]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        return self.rest.get_quote(
            exchange,
            symbol,
        )

    # =====================================================
    # Time Price Series
    # =====================================================

    def get_time_price_series(
        self,
        exchange: str,
        token: str,
        start_time: str,
        interval: int,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        raw_data = self.rest.get_time_price_series(
            exchange,
            token,
            start_time,
            interval,
        )

        return self._normalize_ohlc(
            raw_data
        )

    # =====================================================
    # OHLC Normalization
    # =====================================================

    def _normalize_ohlc(
        self,
        candles: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Convert Flattrade TPSeries candles into the
        canonical AEGIS OHLC format.

        Timestamp is always represented in IST as:

            DD-MM-YYYY HH:MM:SS

        Broker-specific field names remain outside
        the AEGIS data layer.
        """

        normalized: list[dict[str, Any]] = []

        for candle in candles:
            normalized.append(
                self._normalize_candle(
                    candle
                )
            )

        # -----------------------------------------------------
        # Sort candles chronologically
        # Oldest candle first, newest candle last
        # -----------------------------------------------------

        normalized.sort(
            key=lambda candle: datetime.strptime(
                candle["timestamp"],
                "%d-%m-%Y %H:%M:%S",
            )
        )

        return normalized

    def _normalize_candle(
        self,
        candle: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Normalize one raw Flattrade candle.
        """

        timestamp = self._normalize_timestamp(
            candle
        )

        return {
            "timestamp": timestamp,
            "open": self._numeric_value(
                candle.get("into")
            ),
            "high": self._numeric_value(
                candle.get("inth")
            ),
            "low": self._numeric_value(
                candle.get("intl")
            ),
            "close": self._numeric_value(
                candle.get("intc")
            ),
            "volume": self._integer_value(
                candle.get("intv")
            ),
            "oi": self._integer_value(
                candle.get("intoi")
            ),
        }

    # =====================================================
    # Timestamp
    # =====================================================

    def _normalize_timestamp(
        self,
        candle: dict[str, Any],
    ) -> str:
        """
        Convert Flattrade candle timestamp to IST.

        Preferred Flattrade field:

            time

        Expected broker format:

            DD-MM-YYYY HH:MM:SS
        """

        raw_timestamp = (
            candle.get("time")
            or candle.get("timestamp")
        )

        if not raw_timestamp:
            raise ValueError(
                "TPSeries candle has no timestamp."
            )

        if isinstance(
            raw_timestamp,
            (int, float),
        ):

            dt = datetime.fromtimestamp(
                float(raw_timestamp),
                tz=timezone.utc,
            )

            dt = dt.astimezone(
                self._ist
            )

        else:

            raw_timestamp = str(
                raw_timestamp
            ).strip()

            try:

                dt = datetime.strptime(
                    raw_timestamp,
                    "%d-%m-%Y %H:%M:%S",
                )

                dt = dt.replace(
                    tzinfo=self._ist
                )

            except ValueError:

                try:

                    dt = datetime.fromisoformat(
                        raw_timestamp
                    )

                except ValueError as exc:

                    raise ValueError(
                        "Unsupported TPSeries timestamp: "
                        f"{raw_timestamp}"
                    ) from exc

                if dt.tzinfo is None:

                    dt = dt.replace(
                        tzinfo=self._ist
                    )

                else:

                    dt = dt.astimezone(
                        self._ist
                    )

        return dt.strftime(
            "%d-%m-%Y %H:%M:%S"
        )
            # =====================================================
    # Numeric Conversion Helpers
    # =====================================================

    @staticmethod
    def _numeric_value(
        value: Any,
    ) -> float | None:
        """
        Convert a broker numeric value into a float.

        Empty or missing values are represented as None.
        """

        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

        try:
            return float(value)

        except (TypeError, ValueError) as exc:

            raise ValueError(
                f"Invalid numeric market-data value: {value}"
            ) from exc

    @staticmethod
    def _integer_value(
        value: Any,
    ) -> int | None:
        """
        Convert a broker integer value into an int.

        Empty or missing values are represented as None.
        """

        if value is None:
            return None

        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

        try:
            return int(float(value))

        except (TypeError, ValueError) as exc:

            raise ValueError(
                f"Invalid integer market-data value: {value}"
            ) from exc

    # =====================================================
    # Option Chain
    # =====================================================

    def get_option_chain(
        self,
        symbol: str,
        expiry: str,
    ) -> dict[str, Any]:

        raise NotImplementedError(
            "Option Chain API migration pending."
        )

    # =====================================================
    # Historical Data
    # =====================================================

    def get_historical_data(
        self,
        exchange: str,
        symbol: str,
        interval: str,
        start: str,
        end: str,
    ) -> list[dict[str, Any]]:

        if self.rest is None:
            raise RuntimeError(
                "Broker is not authenticated."
            )

        # ------------------------------------------------------
        # Convert AEGIS interval to Flattrade interval
        # ------------------------------------------------------

        interval_map = {
            "1m": 1,
            "3m": 3,
            "5m": 5,
            "10m": 10,
            "15m": 15,
            "30m": 30,
            "60m": 60,
        }

        if interval not in interval_map:
            raise ValueError(
                f"Unsupported historical interval: {interval}"
            )

        flattrade_interval = interval_map[interval]

        # ------------------------------------------------------
        # TPSeries
        #
        # 'symbol' is expected to be the Flattrade token.
        # ------------------------------------------------------

        raw_data = self.rest.get_time_price_series(
            exchange=exchange,
            token=symbol,
            start_time=start,
            interval=flattrade_interval,
        )

        historical_data: list[dict[str, Any]] = []

        # ------------------------------------------------------
        # Normalize Flattrade response into AEGIS format
        # ------------------------------------------------------

        for candle in raw_data:

            raw_timestamp = (
                candle.get("time")
                or candle.get("timestamp")
                or ""
            )

            if not raw_timestamp:
                continue

            # Flattrade commonly returns:
            #
            # 11:16:00 11-08-2026
            #
            # AEGIS standard:
            #
            # 11-08-2026 11:16:00
            #
            timestamp = raw_timestamp.strip()

            try:

                parsed_time = time.strptime(
                    timestamp,
                    "%H:%M:%S %d-%m-%Y",
                )

                timestamp = time.strftime(
                    "%d-%m-%Y %H:%M:%S",
                    parsed_time,
                )

            except ValueError:

                try:

                    parsed_time = time.strptime(
                        timestamp,
                        "%d-%m-%Y %H:%M:%S",
                    )

                    timestamp = time.strftime(
                        "%d-%m-%Y %H:%M:%S",
                        parsed_time,
                    )

                except ValueError:
                    continue

            # --------------------------------------------------
            # Normalize numeric fields
            # --------------------------------------------------

            try:
                open_price = float(candle.get("into", 0))
                high_price = float(candle.get("inth", 0))
                low_price = float(candle.get("intl", 0))
                close_price = float(candle.get("intc", 0))
                volume = int(float(candle.get("intv", 0)))
                open_interest = int(
                    float(candle.get("intoi", 0))
                )

            except (TypeError, ValueError):
                continue

            historical_data.append(
                {
                    "timestamp": timestamp,
                    "open": open_price,
                    "high": high_price,
                    "low": low_price,
                    "close": close_price,
                    "volume": volume,
                    "oi": open_interest,
                }
            )

        # ------------------------------------------------------
        # Optional end-time filtering
        # ------------------------------------------------------

        if end:

            try:

                end_dt = time.strptime(
                    end,
                    "%d-%m-%Y %H:%M:%S",
                )

                end_timestamp = time.mktime(end_dt)

                filtered_data = []

                for candle in historical_data:

                    candle_dt = time.strptime(
                        candle["timestamp"],
                        "%d-%m-%Y %H:%M:%S",
                    )

                    if time.mktime(candle_dt) <= end_timestamp:
                        filtered_data.append(candle)

                historical_data = filtered_data

            except ValueError:
                pass

        # ------------------------------------------------------
        # Sort candles chronologically
        # Oldest candle first, newest candle last
        # ------------------------------------------------------

        historical_data.sort(
            key=lambda candle: time.strptime(
                candle["timestamp"],
                "%d-%m-%Y %H:%M:%S",
            )
        )

        return historical_data







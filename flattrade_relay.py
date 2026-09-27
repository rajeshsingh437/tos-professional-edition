"""
AEGIS Flattrade to Telegram Signal Relay
Monitors Flattrade terminal orders and automatically broadcasts
'buy ce', 'buy pe', or 'exit' signals to Telegram.
"""

from __future__ import annotations

import os
import sys
import time
import json
import asyncio
import re
import typing
from pathlib import Path
from dotenv import load_dotenv

# Ensure root and src are on path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from telethon import TelegramClient

try:
    from brokers.flattrade.rest import RestClient, RestClientError
except ImportError:
    from src.brokers.flattrade.rest import RestClient, RestClientError

try:
    from config.settings import load_broker, load_session, save_session
except ImportError:
    from ..config.settings import load_broker, load_session, save_session  # type: ignore[import-not-found]

load_dotenv()

# --- Telegram Configuration ---
TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID") or 0)
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH") or ""
TARGET_GROUP = os.getenv("TELEGRAM_TARGET_GROUP") or ""
SESSION_NAME = "trade_user"

# --- Relay Configuration ---
# Set to True for interactive confirmation prompt in Saved Messages ('me')
# Set to False to immediately forward to group on fill
REQUIRE_CONFIRMATION = os.getenv("FLATTRADE_REQUIRE_CONFIRMATION", "false").lower() in ("true", "1", "yes")

# Casing convention: "lower" ("buy ce", "exit") or "upper" ("BUY CE", "EXIT")
SIGNAL_CASING = os.getenv("SIGNAL_CASING", "lower")

def format_signal(action: str) -> str:
    """Format signal according to configured casing."""
    return action.lower() if SIGNAL_CASING == "lower" else action.upper()

def get_option_type(order: dict) -> str | None:
    """
    Detects whether an option order is CE (Call) or PE (Put)
    irrespective of weekly or monthly contract expiry, strike, or exchange.
    Checks:
      1. Broker API explicit option type ('optt' / 'opt_type')
      2. Display / contract name ('dname', 'cname')
      3. Trading symbol ('tsym') for both NSE weekly/monthly symbols (e.g. NIFTY2692424500CE)
         and NorenAPI symbols (e.g. NIFTY26924C24500).
    """
    # 1. Direct API field from Flattrade/NorenAPI (if available)
    optt = str(order.get("optt") or order.get("opt_type") or "").strip().upper()
    if optt in ("CE", "CA", "CALL"):
        return "CE"
    if optt in ("PE", "PA", "PUT"):
        return "PE"

    # 2. Check descriptive / contract names (e.g. 'NIFTY 24SEP26 24500 CE ', 'BANKNIFTY 25 SEP 26 54000 CALL')
    dname = str(order.get("dname") or "").strip().upper()
    cname = str(order.get("cname") or "").strip().upper()
    for name in (dname, cname):
        if not name:
            continue
        if re.search(r"\b(CE|CALL)\b", name) or name.endswith("CE"):
            return "CE"
        if re.search(r"\b(PE|PUT)\b", name) or name.endswith("PE"):
            return "PE"

    # 3. Check trading symbol (clean of spaces)
    tsym = str(order.get("tsym") or "").strip().upper()
    if not tsym:
        return None

    # Check if symbol ends with CE or PE (standard NSE weekly & monthly format: e.g. NIFTY2692424500CE)
    if tsym.endswith("CE"):
        return "CE"
    if tsym.endswith("PE"):
        return "PE"

    # Check NorenAPI format where strike is preceded by C or P (e.g. NIFTY26924C24500)
    if re.search(r"C\d+(?:\.0+)?$", tsym):
        return "CE"
    if re.search(r"P\d+(?:\.0+)?$", tsym):
        return "PE"

    return None

def map_order_to_signal(order: dict) -> str | None:
    """
    Translates completed Flattrade order to Telegram signal:
    Buy CE (weekly/monthly) -> buy ce
    Buy PE (weekly/monthly) -> buy pe
    Sell (square-off/exit)  -> exit
    """
    opt_type = get_option_type(order)
    trantype = str(order.get("trantype") or "").strip().upper()  # 'B' (Buy) or 'S' (Sell)

    if trantype == "B":
        if opt_type == "CE":
            return format_signal("buy ce")
        elif opt_type == "PE":
            return format_signal("buy pe")
    elif trantype == "S":
        # Only trigger exit if this was an option trade (or in derivatives segment NFO/BFO/MCX)
        if opt_type or str(order.get("exch") or "").upper() in ("NFO", "BFO", "MCX"):
            return format_signal("exit")

    return None

class FlattradeTelegramRelay:
    def __init__(self) -> None:
        self.broker_cfg = load_broker()
        self.session_cfg = load_session()
        self.tg_client = TelegramClient(SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
        self.processed_order_ids: set[str] = set()
        self.rest_client: RestClient | None = None
        self.target_chat = int(TARGET_GROUP) if TARGET_GROUP.lstrip("-").isdigit() else TARGET_GROUP

    def init_rest_client(self) -> bool:
        """Initializes RestClient with saved session and verifies connection."""
        self.session_cfg = load_session()
        token = self.session_cfg.get("access_token", "")
        client_id = self.session_cfg.get("client_id", "") or self.broker_cfg.get("client_id", "")
        
        if not token or not client_id:
            print("[AUTH ERROR] No active Flattrade session token found in config/session.json")
            return False
            
        self.rest_client = RestClient(access_token=token, client_id=client_id)
        
        try:
            limits = self.rest_client.get_limits()
            if isinstance(limits, dict) and limits.get("stat") == "Ok":
                print(f"[AUTH OK] Flattrade session verified for Client: {client_id}")
                return True
            print(f"[AUTH WARNING] Limits check response: {limits}")
            return True
        except RestClientError as e:
            print(f"[SESSION EXPIRED] {e}")
            return False

    async def broadcast_to_group(self, signal: str):
        """Sends signal to target Telegram group."""
        await self.tg_client.send_message(self.target_chat, signal)
        print(f"\n>>> [BROADCAST SENT]: '{signal}' -> {self.target_chat} <<<\n")

    async def ask_confirmation_and_send(self, signal: str, order_details: str):
        """Sends confirmation request to user's Saved Messages ('me')."""
        alert_text = (
            f"⚡ **Flattrade Order Fill Detected**\n\n"
            f"**Details:** `{order_details}`\n"
            f"**Proposed Signal:** `{signal}`\n\n"
            f"Reply **`Y`** to broadcast to group, or any other key to cancel.\n"
            f"*(Auto-timeout in 20 seconds)*"
        )
        await self.tg_client.send_message("me", alert_text)
        print(f"[CONFIRMATION PROMPT]: Sent prompt for '{signal}' to Telegram Saved Messages.")

        start_time = time.time()
        confirmed = False
        while time.time() - start_time < 20:
            msgs = await self.tg_client.get_messages("me", limit=1)
            msg_list = msgs if isinstance(msgs, list) else ([msgs] if msgs else [])
            if msg_list:
                latest: typing.Any = msg_list[0]
                if getattr(latest, "date", None) and latest.date.timestamp() > start_time and getattr(latest, "message", None):
                    text = str(latest.message).strip().upper()
                    if text == "Y":
                        confirmed = True
                        break
                    else:
                        print(f"[CANCELLED]: Received reply '{text}'.")
                        break
            await asyncio.sleep(0.8)

        if confirmed:
            await self.broadcast_to_group(signal)
            await self.tg_client.send_message("me", f"✅ Broadcasted: `{signal}`")
        else:
            await self.tg_client.send_message("me", f"❌ Signal timed out or cancelled (`{signal}`).")

    def sync_existing_orders(self):
        """Pulls existing completed orders on startup so past orders aren't re-sent."""
        if not self.rest_client:
            return
        try:
            orders = self.rest_client.get_orders()
            if isinstance(orders, list):
                for ord_item in orders:
                    ord_id = ord_item.get("norenordno")
                    if ord_id:
                        self.processed_order_ids.add(str(ord_id))
            print(f"[INITIAL SYNC]: Loaded {len(self.processed_order_ids)} existing orders from Flattrade orderbook.")
        except Exception as e:
            if "no data" in str(e).lower():
                print("[INITIAL SYNC]: Order book is empty (0 orders placed today so far).")
            else:
                print(f"[WARNING]: Could not fetch initial order book: {e}")

    async def run(self):
        """Main monitoring loop."""
        print("=" * 60)
        print("     AEGIS FLATTRADE -> TELEGRAM RELAY")
        print("=" * 60)
        print(f"Target Group ID      : {self.target_chat}")
        print(f"Signal Casing        : {SIGNAL_CASING}")
        print(f"Require Confirmation : {REQUIRE_CONFIRMATION}")
        print("=" * 60)

        # 1. Connect Telegram Userbot
        start_result = typing.cast(typing.Awaitable[typing.Any], self.tg_client.start())  # type: ignore[not-async]
        if asyncio.iscoroutine(start_result) or hasattr(start_result, "__await__"):
            await start_result
        print("[TELEGRAM] Connected as Userbot.")

        # 2. Check Flattrade Session (Auto-login if expired)
        if not self.init_rest_client():
            print("\n[SESSION EXPIRED / NOT FOUND] Launching Flattrade login...")
            try:
                from flattrade_login import login_today
            except ImportError:
                from .flattrade_login import login_today  # type: ignore[import-not-found]
            if not login_today() or not self.init_rest_client():
                print("\n[ERROR] Could not authenticate with Flattrade. Exiting.")
                return

        if not self.rest_client:
            print("\n[ERROR] Flattrade RestClient failed to initialize. Exiting.")
            return

        # 3. Synchronize existing order book
        self.sync_existing_orders()

        print("\n[*] Monitoring Flattrade terminal orders for new fills... (Press Ctrl+C to stop)\n")

        # 4. Polling loop
        while True:
            try:
                orders = self.rest_client.get_orders()
                if isinstance(orders, list):
                    for order in orders:
                        ord_id = str(order.get("norenordno", ""))
                        status = order.get("status", "").upper()

                        if status == "COMPLETE" and ord_id and ord_id not in self.processed_order_ids:
                            self.processed_order_ids.add(ord_id)
                            signal = map_order_to_signal(order)
                            
                            if signal:
                                tsym = order.get("tsym", "")
                                side = order.get("trantype", "")
                                qty = order.get("qty", "")
                                price = order.get("avgprc", order.get("prc", ""))
                                details = f"{tsym} {side} {qty} @ {price}"

                                print(f"\n[NEW FILL DETECTED]: {details} --> Signal: '{signal}'")

                                if REQUIRE_CONFIRMATION:
                                    await self.ask_confirmation_and_send(signal, details)
                                else:
                                    await self.broadcast_to_group(signal)

            except RestClientError as rce:
                if "no data" not in str(rce).lower():
                    print(f"[Flattrade API Alert]: {rce}")
            except Exception as e:
                if "no data" not in str(e).lower():
                    print(f"[Polling Error]: {e}")

            await asyncio.sleep(1.0)

    async def run_test_mode(self):
        """Runs offline/closed-market verification of Telegram, Flattrade session, and weekly options parser."""
        print("=" * 65)
        print("      AEGIS FLATTRADE RELAY - TEST & VERIFICATION MODE")
        print("=" * 65)
        print(f"Target Group ID      : {self.target_chat}")
        print(f"Signal Casing        : {SIGNAL_CASING}")
        print(f"Require Confirmation : {REQUIRE_CONFIRMATION}")
        print("-" * 65)

        # 1. Test Telegram Connection
        print("[1/3] Testing Telegram Connection...")
        try:
            start_result = typing.cast(typing.Awaitable[typing.Any], self.tg_client.start())  # type: ignore[not-async]
            if asyncio.iscoroutine(start_result) or hasattr(start_result, "__await__"):
                await start_result
            me = await self.tg_client.get_me()
            name = getattr(me, "first_name", "User")
            username = f"(@{me.username})" if getattr(me, "username", None) else ""
            print(f"  [OK] Telegram connected successfully as: {name} {username} [ID: {getattr(me, 'id', 'N/A')}]")
        except Exception as e:
            print(f"  [ERROR] Telegram connection error: {e}")

        # 2. Test Flattrade Session
        print("\n[2/3] Checking Flattrade API Session Status...")
        session_loaded = self.init_rest_client()
        if session_loaded:
            print("  [OK] Flattrade API session is currently ACTIVE.")
        else:
            print("  [INFO] Flattrade session is expired or inactive (normal when market is closed).")
            print("         On trading days, run 'python flattrade_login.py' before market open to refresh.")

        # 3. Simulate Weekly Option Orders
        print("\n[3/3] Simulating Weekly Option Order Fills (irrespective of expiry):")
        test_cases: list[tuple[str, dict[str, str]]] = [
            (
                "NIFTY Weekly Call (Buy)",
                {"tsym": "NIFTY2692424500CE", "trantype": "B", "qty": "75", "prc": "120.50", "status": "COMPLETE"}
            ),
            (
                "NIFTY Weekly Put (Buy)",
                {"tsym": "NIFTY2692424500PE", "trantype": "B", "qty": "75", "prc": "95.00", "status": "COMPLETE"}
            ),
            (
                "Weekly Call Square-off (Exit / Sell)",
                {"tsym": "NIFTY2692424500CE", "trantype": "S", "qty": "75", "prc": "165.00", "status": "COMPLETE", "exch": "NFO"}
            ),
            (
                "BANKNIFTY Weekly Call (Buy)",
                {"tsym": "BANKNIFTY2692554000CE", "trantype": "B", "qty": "30", "prc": "250.00", "status": "COMPLETE"}
            ),
            (
                "October Weekly Put (Buy)",
                {"tsym": "NIFTY24O0325000PE", "trantype": "B", "qty": "75", "prc": "110.00", "status": "COMPLETE"}
            ),
        ]

        for lbl, ord_data in test_cases:
            sig = map_order_to_signal(ord_data)
            tsym = ord_data.get("tsym", "")
            side = ord_data.get("trantype", "")
            print(f"  * {lbl:<35} -> Order: {tsym} ({side}) ==> Signal: '{sig}'")

        print("\n" + "=" * 65)
        print("  ALL VERIFICATION TESTS COMPLETED!")
        print("=" * 65)


def main():
    relay = FlattradeTelegramRelay()
    try:
        if len(sys.argv) > 1 and sys.argv[1].lower() in ("--test", "-t", "test"):
            asyncio.run(relay.run_test_mode())
        else:
            asyncio.run(relay.run())
    except KeyboardInterrupt:
        print("\nRelay stopped by user.")


if __name__ == "__main__":
    main()

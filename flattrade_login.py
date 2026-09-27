"""
AEGIS Flattrade Daily Session Login Helper
Run this each morning before market open to generate today's session token.
"""

from __future__ import annotations

import sys
import webbrowser
from pathlib import Path

# Add project root and src to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from src.core.broker.adapters.flattrade_adapter import FlattradeAdapter
from config.settings import load_session

def login_today():
    print("=" * 60)
    print("       AEGIS FLATTRADE DAILY LOGIN HELPER")
    print("=" * 60)
    
    broker = FlattradeAdapter()
    
    # 1. Clear stale session from yesterday so fresh login triggers
    print("[1/3] Clearing stale session...")
    broker.auth.clear()
    
    # 2. Initiate OAuth flow
    print("[2/3] Initiating OAuth flow (opening Flattrade in your browser)...")
    success = broker.login()
    
    if not success:
        print("\n[ERROR] Flattrade login could not be completed.")
        return False
        
    # 3. Verify limits / session
    print("\n[3/3] Verifying session limits with Flattrade...")
    try:
        limits = broker.get_limits()
        print("\n" + "=" * 60)
        print("✅ FLATTRADE LOGIN SUCCESSFUL!")
        print("=" * 60)
        print(f"Client ID     : {broker.auth.state.client_id}")
        print(f"Session Saved : config/session.json")
        if isinstance(limits, dict):
            cash = limits.get("cash", "N/A")
            print(f"Available Cash: {cash}")
        print("=" * 60)
        print("You can now run: python flattrade_relay.py")
        return True
    except Exception as e:
        print(f"[WARNING] Token obtained, but limits check returned: {e}")
        return True

if __name__ == "__main__":
    login_today()

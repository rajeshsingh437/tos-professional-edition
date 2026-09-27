"""
AEGIS

Flattrade Login Smoke Test
"""

from __future__ import annotations

from src.core.broker.adapters.flattrade_adapter import (
    FlattradeAdapter,
)


def main() -> None:

    broker = FlattradeAdapter()

    print("=" * 60)
    print("AEGIS - Flattrade Login Test")
    print("=" * 60)

    print("\nConnecting...")
    broker.connect()

    print(f"Connected: {broker.is_connected()}")

    print("\nChecking authentication...")
    authenticated = broker.login()

    print(f"Authenticated: {authenticated}")

    print("\nBroker Profile")
    print(broker.get_profile())

    if authenticated:

        print("\nFetching Limits...")

        try:
            limits = broker.get_limits()
            print(limits)

        except Exception as error:
            import traceback

            print("\n" + "=" * 60)
            print("LIMITS REQUEST FAILED")
            print("=" * 60)
            print(f"Exception Type : {type(error).__name__}")
            print(f"Exception      : {error}")
            print("\nFull Traceback:\n")
            traceback.print_exc()
            print("=" * 60)

    print("\nDisconnected.")
    print("=" * 60)


if __name__ == "__main__":
    main()

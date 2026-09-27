"""
AEGIS

Application Entry
"""

from ui.main_window import MainWindow

from src.core.broker.broker_manager import BrokerManager


class TOSApplication(MainWindow):
    """
    Root application.

    Responsible for coordinating application services.
    """

    def __init__(self):
        super().__init__()

        # ==========================================
        # Broker Services
        # ==========================================

        self.broker = BrokerManager()

        print("=" * 60)
        print("AEGIS Starting...")
        print("=" * 60)

        print("Initializing Broker Manager...")

        self.broker.start()

        print("Broker Manager initialized.")
        print("Starting Flattrade login...")

        # Login FIRST
        self.broker.login()

        print("Broker login completed.")

        # ==========================================
        # Read-only API Tests
        # ==========================================

        print("\n" + "=" * 60)
        print("LIMITS")
        print("=" * 60)
        print(self.broker.get_limits())

        print("\n" + "=" * 60)
        print("POSITIONS")
        print("=" * 60)
        print(self.broker.get_positions())

        print("\n" + "=" * 60)
        print("ORDERS")
        print("=" * 60)
        print(self.broker.get_orders())

        print("\n" + "=" * 60)
        print("HOLDINGS")
        print("=" * 60)
        print(self.broker.get_holdings())

        print("\n" + "=" * 60)
        print("TRADEBOOK")
        print("=" * 60)
        print(self.broker.get_tradebook())

        print("\n" + "=" * 60)
        print("Read-only API test completed.")
        print("=" * 60)
        print("\n" + "=" * 60)
        print("SEARCH SCRIP TEST")
        print("=" * 60)
        print(
    self.broker.get_quote(
        "NSE",
        "3045",
    )
)
        print("\n" + "=" * 60)
        print("TP SERIES TEST")
        print("=" * 60)

        print(
    self.broker.get_time_price_series(
        "NSE",
        "3045",
        "10-08-2026 09:15:00",
        1,
    )
)






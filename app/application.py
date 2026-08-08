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

        # perform broker login as part of initialization
        self.broker.login()

        print("Broker login completed.")

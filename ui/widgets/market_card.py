"""
AEGIS
Market Snapshot Card
"""

from PySide6.QtWidgets import QLabel

from ui.widgets.card import Card


class MarketCard(Card):
    """
    Displays major market indicators.
    """

    def __init__(self):
        super().__init__("Market Snapshot")

        indices = [
            ("NIFTY 50", "25,120.40", "+0.42%"),
            ("BANK NIFTY", "56,210.75", "+0.18%"),
            ("INDIA VIX", "12.84", "-1.65%"),
            ("USD/INR", "86.21", "+0.07%"),
            ("CRUDE", "$71.82", "-0.54%"),
        ]

        for name, value, change in indices:
            label = QLabel(f"{name:<12}   {value}   {change}")
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 11pt;
                }
            """)
            self.body.addWidget(label)

        self.body.addStretch()

"""
AEGIS
Dashboard Page
"""

from PySide6.QtWidgets import (
    QGridLayout,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.card import Card
from ui.widgets.market_card import MarketCard
from ui.widgets.status_card import StatusCard


class Dashboard(QWidget):
    """
    AEGIS Dashboard
    """

    def __init__(self):
        super().__init__()

        # -------------------------------------------------
        # Main Layout
        # -------------------------------------------------

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # -------------------------------------------------
        # Top Dashboard Row
        # -------------------------------------------------

        top_row = QGridLayout()
        top_row.setHorizontalSpacing(20)
        top_row.setVerticalSpacing(20)

        top_row.addWidget(StatusCard(), 0, 0)
        top_row.addWidget(MarketCard(), 0, 1)
        top_row.addWidget(Card("Risk Today"), 0, 2)

        layout.addLayout(top_row)

        # -------------------------------------------------
        # Future Dashboard Sections
        # -------------------------------------------------

        layout.addStretch()

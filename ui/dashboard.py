"""
TOS Professional Edition
Dashboard Page
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class Dashboard(QWidget):
    """
    Main dashboard placeholder.
    """

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        welcome_card = QFrame()

        card_layout = QVBoxLayout(welcome_card)

        title = QLabel("Welcome to TOS Professional Edition")

        title.setAlignment(Qt.AlignLeft)

        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 700;
                color: white;
            }
        """)

        description = QLabel(
            "Build 0.2.001 – Application Shell\n\n"
            "This is the foundation of the Trading Operating System.\n"
            "Future builds will add the Dashboard, Trading Journal,\n"
            "Analytics, Portfolio, Risk Manager, Reports and Settings."
        )

        description.setWordWrap(True)

        description.setStyleSheet("""
            QLabel {
                font-size: 11pt;
                color: #C7CDD6;
            }
        """)

        card_layout.addWidget(title)
        card_layout.addSpacing(10)
        card_layout.addWidget(description)

        layout.addWidget(welcome_card)
        layout.addStretch()
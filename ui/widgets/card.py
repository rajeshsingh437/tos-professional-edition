"""
AEGIS
Reusable Card Widget
"""

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class Card(QFrame):
    """
    Generic reusable dashboard card.
    """

    def __init__(self, title: str):
        super().__init__()

        self.setObjectName("Card")

        self.setStyleSheet("""
        QFrame#Card {
            background-color: #2D3442;
            border: 1px solid #3A4354;
            border-radius: 12px;
        }

        QLabel#CardTitle {
            color: white;
            font-size: 16px;
            font-weight: bold;
        }
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        layout.addWidget(title_label)

        self.body = QVBoxLayout()
        self.body.setSpacing(10)

        layout.addLayout(self.body)

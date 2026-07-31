"""
AEGIS
Session Status Card
"""

from PySide6.QtWidgets import QLabel

from ui.widgets.card import Card


class StatusCard(Card):
    """
    Displays the overall trading readiness.
    """

    def __init__(self):
        super().__init__("Session Status")

        status = QLabel("🟢 GO FOR TRADING")
        status.setStyleSheet("""
        QLabel {
            color: #4ADE80;
            font-size: 18px;
            font-weight: bold;
        }
        """)

        self.body.addWidget(status)

        for text in (
            "Confidence        86%",
            "Checklist         18 / 20",
            "Risk Status       Normal",
            "Market            Neutral",
        ):
            label = QLabel(text)
            label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 11pt;
            }
            """)
            self.body.addWidget(label)

        self.body.addStretch()

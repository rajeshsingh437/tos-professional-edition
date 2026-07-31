"""
AEGIS
Header Widget
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class Header(QWidget):
    """
    Top application header.
    """

    def __init__(self):
        super().__init__()

        self.setFixedHeight(80)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(2)

        # Title
        title = QLabel("AEGIS")
        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: white;
            }
        """)

        # Subtitle
        subtitle = QLabel("Build 1.0.001")
        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        subtitle.setStyleSheet("""
            QLabel {
                font-size: 10pt;
                color: #9CA3AF;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

"""
AEGIS
Sidebar Navigation
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidget


class Sidebar(QListWidget):
    """
    Left navigation panel.
    """

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")

        self.setFixedWidth(240)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.addItems(
            [
                "🏠  Dashboard",
                "📒  Trading Journal",
                "📈  Analytics",
                "💼  Portfolio",
                "🛡️  Risk Manager",
                "📊  Reports",
                "⚙️  Settings",
            ]
        )

        self.setCurrentRow(0)

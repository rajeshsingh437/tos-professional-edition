"""
TOS Professional Edition
Main Application Window
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.dashboard import Dashboard
from ui.header import Header
from ui.sidebar import Sidebar
from ui.theme import DARK_THEME


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AEGIS")
        self.resize(1600, 900)
        self.setMinimumSize(1280, 720)

        self.setStyleSheet(DARK_THEME)

        self._build_ui()

        self.statusBar().showMessage("Ready")

    def _build_ui(self):
        """
        Build the main application layout.
        """

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)

        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # -----------------------------------------
        # Sidebar
        # -----------------------------------------

        sidebar = Sidebar()

        main_layout.addWidget(sidebar)

        # -----------------------------------------
        # Content Area
        # -----------------------------------------

        content = QFrame()

        content.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        content_layout = QVBoxLayout(content)

        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        content_layout.addWidget(Header())
        content_layout.addWidget(Dashboard(), 1)

        main_layout.addWidget(content, 1)

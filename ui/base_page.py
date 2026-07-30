from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BasePage(QWidget):
    """
    Base class for all application pages.

    Every page in TOS should inherit from this class to ensure
    a consistent layout and styling across the application.
    """

    def __init__(self, title: str):
        super().__init__()

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(24, 24, 24, 24)
        self._layout.setSpacing(20)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        font = QFont()
        font.setPointSize(18)
        font.setBold(True)

        self.title_label.setFont(font)

        self._layout.addWidget(self.title_label)
        self._layout.addStretch()

    @property
    def content_layout(self) -> QVBoxLayout:
        """
        Returns the page layout so child pages can add widgets.
        """
        return self._layout
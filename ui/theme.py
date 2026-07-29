"""
TOS Professional Edition
Dark Theme
"""


DARK_THEME = """
QMainWindow {
    background-color: #1B1E24;
}

QWidget {
    background-color: #1B1E24;
    color: #E6E8EB;
    font-family: "Segoe UI";
    font-size: 10pt;
}

QFrame {
    background-color: #242933;
    border-radius: 8px;
}

QLabel {
    color: #E6E8EB;
    background: transparent;
}

QListWidget {
    background-color: #20242C;
    border: none;
    color: #E6E8EB;
    outline: none;
    padding: 8px;
    font-size: 10pt;
}

QListWidget::item {
    padding: 10px;
    margin: 2px;
    border-radius: 6px;
}

QListWidget::item:selected {
    background-color: #3B82F6;
    color: white;
}

QListWidget::item:hover {
    background-color: #313844;
}

QStatusBar {
    background-color: #20242C;
    color: #AEB6C2;
}

QPushButton {
    background-color: #313844;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 8px 12px;
}

QPushButton:hover {
    background-color: #3C4655;
}
"""
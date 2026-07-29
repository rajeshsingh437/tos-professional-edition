import sys

from PySide6.QtWidgets import QApplication

from app.application import TOSApplication


def main() -> None:
    app = QApplication(sys.argv)

    window = TOSApplication()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
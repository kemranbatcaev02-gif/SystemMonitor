"""System Monitor — точка входа."""
import sys

from PySide6.QtWidgets import QApplication

from styles import STYLE
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

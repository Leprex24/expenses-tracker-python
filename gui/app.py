import sys

from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from tracker.file_ops import file_verification_main, file_verification_recurring, file_verification_budget


def main():
    app = QApplication(sys.argv)
    file_verification_main()
    file_verification_recurring()
    file_verification_budget()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
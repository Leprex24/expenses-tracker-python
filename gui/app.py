import logging
import os
import sys

from PyQt6.QtWidgets import QApplication, QMessageBox
from gui.main_window import MainWindow
from tracker.commands import sync_recurring_expenses
from tracker.data_validation import LOG_PATH, LOGS_DIR
from tracker.file_ops import file_verification_main, file_verification_recurring, file_verification_budget

class guiHandler(logging.Handler):
    def emit(self, record):
        if record.levelno > logging.WARNING:
            QMessageBox.critical(None, "Błąd krytyczny", record.getMessage())
        elif record.levelno == logging.WARNING:
            QMessageBox.warning(None, "Ostrzeżenie", record.getMessage())
        else:
            pass

def main():
    app = QApplication(sys.argv)
    os.makedirs(LOGS_DIR, exist_ok=True)
    file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(guiHandler())
    logger.addHandler(file_handler)
    file_verification_main()
    file_verification_recurring()
    file_verification_budget()
    sync_recurring_expenses()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
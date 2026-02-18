from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem


class NumericItem(QTableWidgetItem):
    def __lt__(self, other):
        return self.data(Qt.ItemDataRole.UserRole) < other.data(Qt.ItemDataRole.UserRole)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QLabel, QDoubleSpinBox, QComboBox, \
    QPushButton, QTableWidgetItem, QMessageBox, QHeaderView

from gui.custom_items import NumericItem
from tracker.data_validation import VALID_CATEGORIES, VALID_FREQUENCIES
from tracker.file_ops import load_recurring_expenses
from tracker.utils import filter_by_amount


class RecurringView(QWidget):
    recurring_edit_requested = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        left_panel = QVBoxLayout()
        self.table = QTableWidget(0, 6)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Opis", "Kwota", "Kategoria", "Częstotliwość"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemDoubleClicked.connect(self.on_row_double_clicked)
        left_panel.addWidget(self.table)
        hbox.addLayout(left_panel, stretch=3)

        right_panel = QVBoxLayout()
        amountfrom_label = QLabel("Kwota od:")
        amountto_label = QLabel("Kwota do:")
        category_label = QLabel("Kategoria:")
        frequency_label = QLabel("Czestotliwość:")

        self.amountfrom_edit = QDoubleSpinBox()
        self.amountfrom_edit.setDecimals(2)
        self.amountfrom_edit.setMaximum(999999.99)
        self.amountto_edit = QDoubleSpinBox()
        self.amountto_edit.setMaximum(999999.99)
        self.amountto_edit.setDecimals(2)
        self.category_edit = QComboBox()
        self.category_edit.addItem("Wszystkie")
        self.category_edit.addItems(VALID_CATEGORIES)
        self.frequency_edit = QComboBox()
        self.frequency_edit.addItem("Wszystkie")
        self.frequency_edit.addItems(VALID_FREQUENCIES)
        filter_button = QPushButton("Filtruj")
        clear_button = QPushButton("Wyczyść filtry")

        right_panel.addWidget(amountfrom_label)
        right_panel.addWidget(self.amountfrom_edit)
        right_panel.addWidget(amountto_label)
        right_panel.addWidget(self.amountto_edit)
        right_panel.addWidget(category_label)
        right_panel.addWidget(self.category_edit)
        right_panel.addWidget(frequency_label)
        right_panel.addWidget(self.frequency_edit)
        right_panel.addWidget(filter_button)
        right_panel.addWidget(clear_button)
        right_panel.addStretch()
        right_panel.setSpacing(10)

        filter_button.clicked.connect(self.apply_filters)
        clear_button.clicked.connect(self.clear_filter)

        hbox.addLayout(right_panel, stretch=1)

    def load_data(self, data=None):
        if data is None:
            data = load_recurring_expenses()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        if not data:
            self.table.setRowCount(1)
            self.table.setSpan(0, 0, 1, 6)
            no_data_item = QTableWidgetItem("Brak wydatków cyklicznych do wyświetlenia")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(0, 0, no_data_item)
            return

        for expense in data:
            row_position = self.table.rowCount()
            self.table.setRowCount(row_position + 1)
            item = QTableWidgetItem()
            item.setData(Qt.ItemDataRole.DisplayRole, int(expense[0]))
            self.table.setItem(row_position, 0, item)
            self.table.setItem(row_position, 1, QTableWidgetItem(expense[1]))
            self.table.setItem(row_position, 2, QTableWidgetItem(expense[2]))
            item = NumericItem(f"{expense[3]} zł")
            item.setData(Qt.ItemDataRole.UserRole, float(expense[3]))
            self.table.setItem(row_position, 3, item)
            self.table.setItem(row_position, 4, QTableWidgetItem(expense[4]))
            self.table.setItem(row_position, 5, QTableWidgetItem(expense[5]))
        self.table.setSortingEnabled(True)
        self.table.sortItems(0, Qt.SortOrder.AscendingOrder)


    def apply_filters(self):
        amount_from = self.amountfrom_edit.value()
        amount_to = self.amountto_edit.value()
        if 0 < amount_from < amount_to:
            QMessageBox.warning(self, "Błąd", "Kwota 'od' nie może być większa niż kwota 'do'")
            return

        category = self.category_edit.currentText()
        frequency = self.frequency_edit.currentText()
        if amount_from == 0:
            amount_from = None
        if amount_to == 0:
            amount_to = None
        all_expenses = load_recurring_expenses()
        filtered_expenses = filter_by_amount(amount_from, amount_to, all_expenses)
        if category != "Wszystkie":
            filtered_expenses = [e for e in filtered_expenses if e[4] == category]
        if frequency != "Wszystkie":
            filtered_expenses = [e for e in filtered_expenses if e[5] == frequency]
        self.load_data(filtered_expenses)

    def clear_filter(self):
        self.amountfrom_edit.setValue(0)
        self.amountto_edit.setValue(0)
        self.category_edit.setCurrentIndex(0)
        self.frequency_edit.setCurrentIndex(0)
        self.load_data()

    def on_row_double_clicked(self, item):
        row = item.row()
        expense_id = self.table.item(row, 0).text()
        date = self.table.item(row, 1).text()
        description = self.table.item(row, 2).text()
        amount = self.table.item(row, 3).data(Qt.ItemDataRole.UserRole)
        category = self.table.item(row, 4).text()
        frequency = self.table.item(row, 5).text()
        data = [expense_id, date, description, amount, category, frequency]
        self.recurring_edit_requested.emit(data)
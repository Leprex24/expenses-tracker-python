from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QLabel, \
    QDateEdit, QComboBox, QPushButton, QDoubleSpinBox, QMessageBox

from gui.custom_items import NumericItem
from tracker.data_validation import VALID_CATEGORIES
from tracker.file_ops import get_all_expenses_main
from tracker.utils import filter_by_date, filter_by_amount


class ExpensesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        left_panel = QVBoxLayout()

        self.table = QTableWidget(0, 5)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setHorizontalHeaderLabels(["ID", "Data", "Opis", "Kwota", "Kategoria"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

        left_panel.addWidget(self.table)

        self.sum_label = QLabel("Suma: 0.00 zł")
        left_panel.addWidget(self.sum_label)

        hbox.addLayout(left_panel, stretch=3)
        right_panel = QVBoxLayout()
        datefrom_label = QLabel('Data od:')
        dateto_label = QLabel('Data do:')
        amountfrom_label = QLabel('Kwota od:')
        amountto_label = QLabel('Kwota do:')
        category_label = QLabel('Kategoria:')

        self.datefrom_edit = QDateEdit()
        self.datefrom_edit.setDate(QDate(2020, 1, 1))
        self.datefrom_edit.setCalendarPopup(True)
        self.datefrom_edit.setMaximumDate(QDate.currentDate())
        self.dateto_edit = QDateEdit()
        self.dateto_edit.setDate(QDate.currentDate())
        self.dateto_edit.setMaximumDate(QDate.currentDate())
        self.dateto_edit.setCalendarPopup(True)
        self.amountfrom_edit = QDoubleSpinBox()
        self.amountfrom_edit.setMaximum(999999.99)
        self.amountfrom_edit.setDecimals(2)
        self.amountto_edit = QDoubleSpinBox()
        self.amountto_edit.setMaximum(999999.99)
        self.amountto_edit.setDecimals(2)
        self.category_edit = QComboBox()
        self.category_edit.addItem("Wszystkie")
        self.category_edit.addItems(VALID_CATEGORIES)
        filter_button = QPushButton('Filtruj')
        clear_filter_button = QPushButton('Wyczyść filtry')

        right_panel.addWidget(datefrom_label)
        right_panel.addWidget(self.datefrom_edit)
        right_panel.addWidget(dateto_label)
        right_panel.addWidget(self.dateto_edit)
        right_panel.addWidget(amountfrom_label)
        right_panel.addWidget(self.amountfrom_edit)
        right_panel.addWidget(amountto_label)
        right_panel.addWidget(self.amountto_edit)
        right_panel.addWidget(category_label)
        right_panel.addWidget(self.category_edit)
        right_panel.addWidget(filter_button)
        right_panel.addWidget(clear_filter_button)
        right_panel.addStretch()
        right_panel.setSpacing(10)


        filter_button.clicked.connect(self.apply_filters)
        clear_filter_button.clicked.connect(self.clear_filters)

        hbox.addLayout(right_panel, stretch=1)

    def load_data(self, data=None):
        if data is None:
            data = get_all_expenses_main()
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        if not data:
            self.table.setRowCount(1)
            self.table.setSpan(0, 0, 1, 5)
            no_data_item = QTableWidgetItem("Brak danych do wyświetlenia")
            no_data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(0, 0, no_data_item)
            self.sum_label.setText("Suma : 0.00 zł")
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
        total = sum(float(expense[3]) for expense in data)
        self.sum_label.setText(f"Suma: {total:.2f} zł")
        self.table.setSortingEnabled(True)
        self.table.sortItems(1, Qt.SortOrder.DescendingOrder)

    def apply_filters(self):
        date_from = self.datefrom_edit.date().toString("yyyy-MM-dd")
        date_to = self.dateto_edit.date().toString("yyyy-MM-dd")

        if date_from > date_to:
            QMessageBox.warning(self, "Błąd", "Data 'od' nie może być późniejsza niż data 'do'")
            return

        amount_from = self.amountfrom_edit.value()
        amount_to = self.amountto_edit.value()

        if 0 < amount_to < amount_from:
            QMessageBox.warning(self, "Błąd", "Kwota 'od' nie może być większa niż kwota 'do'")
            return

        category = self.category_edit.currentText()
        all_expenses = get_all_expenses_main()
        filtered_expenses = filter_by_date(date_from, date_to, all_expenses, None)
        if amount_from == 0:
            amount_from = None
        if amount_to == 0:
            amount_to = None
        filtered_expenses = filter_by_amount(amount_from, amount_to, filtered_expenses)
        if category != "Wszystkie":
            filtered_expenses = [e for e in filtered_expenses if e[4] == category]
        self.load_data(filtered_expenses)

    def clear_filters(self):
        self.datefrom_edit.setDate(QDate(2020, 1, 1))
        self.dateto_edit.setDate(QDate.currentDate())
        self.amountfrom_edit.setValue(0)
        self.amountto_edit.setValue(0)
        self.category_edit.setCurrentIndex(0)
        self.load_data()



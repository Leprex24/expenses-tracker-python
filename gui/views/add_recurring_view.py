from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QDoubleSpinBox, \
    QDateTimeEdit, QDateEdit, QComboBox, QPushButton, QMessageBox

from tracker.commands import add_recurring_expense
from tracker.data_validation import VALID_CATEGORIES, VALID_FREQUENCIES
from tracker.validators import validate_recurring_add


class AddRecurringView(QWidget):
    recurring_expense_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addStretch(1)

        container = QWidget()
        container.setMaximumWidth(500)
        form = QVBoxLayout()
        container.setLayout(form)
        form.addStretch(1)

        title_label = QLabel("Dodaj nowy wydatek cykliczny")
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addWidget(title_label)
        form.addSpacing(10)

        self.description_edit = QLineEdit()
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setMaximum(999999.99)
        self.amount_edit.setDecimals(2)
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMaximumDate(QDate.currentDate())
        self.category_edit = QComboBox()
        self.category_edit.addItems(VALID_CATEGORIES)
        self.category_edit.setCurrentIndex(1)
        self.frequency_edit = QComboBox()
        self.frequency_edit.addItems(VALID_FREQUENCIES)
        self.frequency_edit.setCurrentIndex(3)
        add_recurring_button = QPushButton("Dodaj wydatek cykliczny")
        reset_button = QPushButton("Resetuj")

        form.addWidget(QLabel("Opis:"))
        form.addWidget(self.description_edit)
        form.addWidget(QLabel("Kwota:"))
        form.addWidget(self.amount_edit)
        form.addWidget(QLabel("Data:"))
        form.addWidget(self.date_edit)
        form.addWidget(QLabel("Kategoria:"))
        form.addWidget(self.category_edit)
        form.addWidget(QLabel("Częstotliwość:"))
        form.addWidget(self.frequency_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_recurring_button)
        button_layout.addWidget(reset_button)
        form.addLayout(button_layout)
        form.addStretch(1)

        add_recurring_button.clicked.connect(self.add_recurring)
        reset_button.clicked.connect(self.reset_form)

        main_layout.addWidget(container, stretch=2)
        main_layout.addStretch(1)

    def add_recurring(self):
        description = self.description_edit.text()
        amount = self.amount_edit.value()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.category_edit.currentText()
        frequency = self.frequency_edit.currentText()

        valid, error_msg = validate_recurring_add(description, amount, date, category, frequency)
        if not valid:
            QMessageBox.warning(self, "Błąd", error_msg)
            return

        expense_id = add_recurring_expense(description, amount, frequency, date, category)
        self.recurring_expense_added.emit()
        QMessageBox.information(self, "Sukces", f"Wydatek cykliczny o ID: {expense_id} został pomyślnie dodany")
        self.reset_form()

    def reset_form(self):
        self.description_edit.clear()
        self.amount_edit.setValue(0.00)
        self.date_edit.setDate(QDate.currentDate())
        self.category_edit.setCurrentIndex(1)
        self.frequency_edit.setCurrentIndex(3)
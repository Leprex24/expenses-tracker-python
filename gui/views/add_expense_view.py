from PyQt6.QtCore import QDate, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLineEdit, QDoubleSpinBox, QDateEdit, QComboBox, QPushButton, \
    QHBoxLayout, QVBoxLayout, QLabel, QMessageBox

from tracker.commands import add_expense
from tracker.data_validation import VALID_CATEGORIES
from tracker.validators import validate_add


class AddExpenseView(QWidget):
    expense_added = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        main_layout.addStretch(1)

        container = QWidget()
        container.setMaximumWidth(500)
        form = QVBoxLayout()
        container.setLayout(form)
        form.addStretch(1)

        title_label = QLabel("Dodaj nowy wydatek")
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
        add_expense_button = QPushButton("Dodaj wydatek")
        reset_button = QPushButton("Resetuj")

        form.addWidget(QLabel("Opis:"))
        form.addWidget(self.description_edit)
        form.addWidget(QLabel("Kwota:"))
        form.addWidget(self.amount_edit)
        form.addWidget(QLabel("Data:"))
        form.addWidget(self.date_edit)
        form.addWidget(QLabel("Kategoria:"))
        form.addWidget(self.category_edit)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_expense_button)
        button_layout.addWidget(reset_button)
        form.addLayout(button_layout)
        form.addStretch(1)

        add_expense_button.clicked.connect(self.add_expense_gui)
        reset_button.clicked.connect(self.reset_form)

        main_layout.addWidget(container, stretch=2)
        main_layout.addStretch(1)

    def add_expense_gui(self):
        description = self.description_edit.text()
        amount = self.amount_edit.value()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.category_edit.currentText()

        valid, error_msg = validate_add(description, amount, date, category)
        if not valid:
            QMessageBox.warning(self, "Błąd", error_msg)
            return

        expense_id = add_expense(description, amount, date, category)
        self.expense_added.emit()
        QMessageBox.information(self, "Sukces", f"Wydatek o ID: {expense_id} został pomyślnie dodany")
        self.reset_form()

    def reset_form(self):
        self.description_edit.clear()
        self.amount_edit.setValue(0.00)
        self.date_edit.setDate(QDate.currentDate())
        self.category_edit.setCurrentIndex(1)


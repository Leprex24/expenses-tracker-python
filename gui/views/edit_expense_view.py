from PyQt6.QtCore import pyqtSignal, Qt, QDate
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QDoubleSpinBox, QDateEdit, \
    QPushButton, QMessageBox

from tracker.commands import delete_expense, edit_expense
from tracker.data_validation import VALID_CATEGORIES
from tracker.file_ops import get_all_expenses_main
from tracker.validators import validate_delete, validate_edit


class EditExpenseView(QWidget):
    expense_edited = pyqtSignal()
    back_requested = pyqtSignal()
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

        title_label = QLabel("Edytuj wydatek")
        title_font = title_label.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form.addWidget(title_label)
        form.addSpacing(10)

        self.all_expenses = get_all_expenses_main()
        if not self.all_expenses:
            form.addWidget(QLabel("Brak wydatków do edycji"))
        else:
            self.id_list = [str(expense[0]) for expense in self.all_expenses]
            self.id_edit = QComboBox()
            self.id_edit.addItems(self.id_list)
            self.id_edit.currentIndexChanged.connect(self.id_edit_changed)
            self.description_edit = QLineEdit()
            self.amount_edit = QDoubleSpinBox()
            self.amount_edit.setMaximum(999999.99)
            self.amount_edit.setDecimals(2)
            self.date_edit = QDateEdit()
            self.date_edit.setCalendarPopup(True)
            self.date_edit.setMaximumDate(QDate.currentDate())
            self.category_edit = QComboBox()
            self.category_edit.addItems(VALID_CATEGORIES)
            self.current_expense = next(i for i in self.all_expenses if str(i[0]) == self.id_edit.currentText())
            self.load_expense()
            edit_expense_button = QPushButton("Zapisz zmiany")
            reset_expense_button = QPushButton("Resetuj edytowanie")
            delete_expense_button = QPushButton("Usuń wydatek")
            self.back_button = QPushButton("Powrót do listy")
            self.back_button.setVisible(False)

            form.addWidget(QLabel("Wybierz ID wydatku do edycji:"))
            form.addWidget(self.id_edit)
            form.addWidget(QLabel("Opis:"))
            form.addWidget(self.description_edit)
            form.addWidget(QLabel("Kwota:"))
            form.addWidget(self.amount_edit)
            form.addWidget(QLabel("Data:"))
            form.addWidget(self.date_edit)
            form.addWidget(QLabel("Kategoria:"))
            form.addWidget(self.category_edit)
            button_layout = QHBoxLayout()
            button_layout.addWidget(edit_expense_button)
            button_layout.addWidget(reset_expense_button)
            button_layout.addWidget(delete_expense_button)
            button_layout.addWidget(self.back_button)
            form.addLayout(button_layout)
            form.addStretch(1)

            edit_expense_button.clicked.connect(self.edit_expense_gui)
            reset_expense_button.clicked.connect(self.load_expense)
            delete_expense_button.clicked.connect(self.delete_expense_gui)
            self.back_button.clicked.connect(self.back_to_list)

            main_layout.addWidget(container, stretch=2)
            main_layout.addStretch(1)


    def id_edit_changed(self):
        self.current_expense = next(i for i in self.all_expenses if str(i[0]) == self.id_edit.currentText())
        self.load_expense()

    def load_expense(self):
        self.description_edit.setText(self.current_expense[2])
        self.amount_edit.setValue(float(self.current_expense[3]))
        self.date_edit.setDate(QDate.fromString(self.current_expense[1], "yyyy-MM-dd"))
        if self.current_expense[4] in VALID_CATEGORIES:
            self.category_edit.setCurrentText(self.current_expense[4])
        else:
            self.category_edit.setCurrentIndex(0)

    def load_from_table(self, data):
        self.current_expense = data
        self.id_edit.setCurrentText(data[0])
        self.id_edit.setEnabled(False)
        self.back_button.setVisible(True)
        self.load_expense()

    def delete_expense_gui(self):
        expense_id = self.id_edit.currentText()
        valid, error_msg = validate_delete(int(expense_id))
        if not valid:
            QMessageBox.warning(self, "Błąd", error_msg)
            return
        confirm = QMessageBox.question(self, "Potwierdzenie", f"Czy na pewno chcesz usunąć wydatek o ID: {expense_id}?", QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        if confirm == QMessageBox.StandardButton.Ok:
            if delete_expense(int(expense_id)):
                QMessageBox.information(self, "Sukces", f"Wydatek o ID: {expense_id} został pomyślnie usunięty")
                self.expense_edited.emit()
                self.back_to_list()
            else:
                QMessageBox.warning(self, "Błąd", f"Nie można usunąć wydatku o ID: {expense_id}")

    def edit_expense_gui(self):
        expense_id = self.id_edit.currentText()
        description = self.description_edit.text()
        amount = self.amount_edit.value()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        category = self.category_edit.currentText()

        valid, error_msg = validate_edit(description, amount, date, int(expense_id), category)
        if not valid:
            QMessageBox.warning(self, "Błąd", error_msg)
            return
        if edit_expense(description, amount, date, int(expense_id), category):
            QMessageBox.information(self, "Sukces", f"Wydatek o ID: {expense_id} został pomyślnie zaktualizowany")
            self.expense_edited.emit()
        else:
            QMessageBox.warning(self, "Błąd", f"Nie można zaktualizować wydatku o ID: {expense_id}")

    def back_to_list(self):
        self.back_requested.emit()


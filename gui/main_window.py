from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QStackedWidget, QLabel

from gui.views.add_expense_view import AddExpenseView
from gui.views.expenses_view import ExpensesView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker")
        self.setMinimumSize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.expenses_list_view = ExpensesView()
        self.expenses_add_view = AddExpenseView()
        self.expenses_edit_view = QLabel("Edytuj wydatek")
        self.expenses_delete_view = QLabel("Usuń wydatek")

        self.expenses_add_view.expense_added.connect(self.expenses_list_view.load_data)

        self.stack.addWidget(self.expenses_list_view)
        self.stack.addWidget(self.expenses_add_view)
        self.stack.addWidget(self.expenses_edit_view)
        self.stack.addWidget(self.expenses_delete_view)

        expenses_menu = self.menuBar().addMenu("Wydatki")
        expenses_list_action = expenses_menu.addAction("Lista wydatków")
        expenses_add_action = expenses_menu.addAction("Dodaj wydatek")
        expenses_edit_action = expenses_menu.addAction("Edytuj wydatek")
        expenses_delete_action = expenses_menu.addAction("Usuń wydatek")

        expenses_list_action.triggered.connect(self.show_expenses_list)
        expenses_add_action.triggered.connect(self.show_expenses_add)

    def show_expenses_list(self):
        self.stack.setCurrentIndex(0)

    def show_expenses_add(self):
        self.stack.setCurrentIndex(1)



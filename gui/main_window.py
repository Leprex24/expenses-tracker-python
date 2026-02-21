from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QStackedWidget, QLabel

from gui.views.add_expense_view import AddExpenseView
from gui.views.edit_expense_view import EditExpenseView
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
        self.expenses_edit_view = EditExpenseView()

        self.expenses_list_view.edit_requested.connect(self.open_edit_view)
        self.expenses_add_view.expense_added.connect(self.expenses_list_view.load_data)
        self.expenses_edit_view.expense_edited.connect(self.expenses_list_view.load_data)
        self.expenses_edit_view.back_requested.connect(self.show_expenses_list)

        self.stack.addWidget(self.expenses_list_view)
        self.stack.addWidget(self.expenses_add_view)
        self.stack.addWidget(self.expenses_edit_view)

        expenses_menu = self.menuBar().addMenu("Wydatki")
        expenses_list_action = expenses_menu.addAction("Lista wydatków")
        expenses_add_action = expenses_menu.addAction("Dodaj wydatek")
        expenses_edit_action = expenses_menu.addAction("Edytuj wydatek")

        expenses_list_action.triggered.connect(self.show_expenses_list)
        expenses_add_action.triggered.connect(self.show_expenses_add)
        expenses_edit_action.triggered.connect(self.show_expenses_edit)

    def show_expenses_list(self):
        self.stack.setCurrentIndex(0)

    def show_expenses_add(self):
        self.stack.setCurrentIndex(1)

    def show_expenses_edit(self):
        self.stack.setCurrentIndex(2)

    def open_edit_view(self, data):
        self.expenses_edit_view.load_from_table(data)
        self.show_expenses_edit()



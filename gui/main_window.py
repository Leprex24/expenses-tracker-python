from PyQt6.QtWidgets import QMainWindow, QTabWidget, QWidget, QStackedWidget, QLabel

from gui.views.add_expense_view import AddExpenseView
from gui.views.add_recurring_view import AddRecurringView
from gui.views.edit_expense_view import EditExpenseView
from gui.views.edit_recurring_view import EditRecurringView
from gui.views.expenses_view import ExpensesView
from gui.views.recurring_view import RecurringView


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
        self.recurring_list_view = RecurringView()
        self.recurring_add_view = AddRecurringView()
        self.recurring_edit_view = EditRecurringView()

        self.expenses_list_view.edit_requested.connect(self.open_edit_view)
        self.expenses_add_view.expense_added.connect(self.expenses_list_view.load_data)
        self.expenses_edit_view.expense_edited.connect(self.expenses_list_view.load_data)
        self.expenses_edit_view.back_requested.connect(self.show_expenses_list)
        self.recurring_list_view.recurring_edit_requested.connect(self.open_recurring_edit_view)
        self.recurring_add_view.recurring_expense_added.connect(self.recurring_list_view.load_data)
        self.recurring_edit_view.recurring_expense_edited.connect(self.recurring_list_view.load_data)
        self.recurring_edit_view.recurring_back_requested.connect(self.show_recurring_list)


        self.stack.addWidget(self.expenses_list_view)
        self.stack.addWidget(self.expenses_add_view)
        self.stack.addWidget(self.expenses_edit_view)
        self.stack.addWidget(self.recurring_list_view)
        self.stack.addWidget(self.recurring_add_view)
        self.stack.addWidget(self.recurring_edit_view)

        expenses_menu = self.menuBar().addMenu("Wydatki")
        expenses_list_action = expenses_menu.addAction("Lista wydatków")
        expenses_add_action = expenses_menu.addAction("Dodaj wydatek")
        expenses_edit_action = expenses_menu.addAction("Edytuj wydatek")

        recurring_menu = self.menuBar().addMenu("Wydatki cykliczne")
        recurring_list_action = recurring_menu.addAction("Lista wydatków cyklicznych")
        recurring_add_action = recurring_menu.addAction("Dodaj wydatek cykliczny")
        recurring_edit_action = recurring_menu.addAction("Edytuj wydatek cykliczny")

        expenses_list_action.triggered.connect(self.show_expenses_list)
        expenses_add_action.triggered.connect(self.show_expenses_add)
        expenses_edit_action.triggered.connect(self.show_expenses_edit)
        recurring_list_action.triggered.connect(self.show_recurring_list)
        recurring_add_action.triggered.connect(self.show_recurring_add)
        recurring_edit_action.triggered.connect(self.show_recurring_edit)

    def show_expenses_list(self):
        self.stack.setCurrentIndex(0)

    def show_expenses_add(self):
        self.stack.setCurrentIndex(1)

    def show_expenses_edit(self):
        self.expenses_edit_view.reset_to_default()
        self.stack.setCurrentIndex(2)

    def open_edit_view(self, data):
        self.expenses_edit_view.load_from_table(data)
        self.stack.setCurrentIndex(2)

    def show_recurring_list(self):
        self.stack.setCurrentIndex(3)

    def show_recurring_add(self):
        self.stack.setCurrentIndex(4)

    def show_recurring_edit(self):
        self.recurring_edit_view.reset_to_default()
        self.stack.setCurrentIndex(5)

    def open_recurring_edit_view(self, data):
        self.recurring_edit_view.load_from_table(data)
        self.stack.setCurrentIndex(5)

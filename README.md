# Expense Tracker
A Python application for tracking personal expenses, available both as a command-line tool and a graphical interface (GUI).

## Features

* Add, list, edit and delete expenses
* Recurring expenses with automatic syncing
* Monthly budget management with reporting (not yet implemented in GUI) 
* Expense summaries and statistics by category or date range (not yet implemented in GUI) 
* Full monthly reports combining expenses, budget and recurring data (not yet implemented in GUI) 
* Export to CSV, JSON or XLSX (not yet implemented in GUI) 
* Data validation and automatic backups
* Data stored in local CSV files

---

## Running the App

### GUI

```
python main_gui.py
```
### CLI
```
python -m tracker.main [command] [options]
```

---

## CLI Commands

### Expenses (`wydatki`)

| Command | Description | Example |
|---|---|---|
| `dodaj` | Add an expense | `python -m tracker.main dodaj -o "Bread" -k 7.50 --kategoria Jedzenie` |
| `wypisz` | List expenses | `python -m tracker.main wypisz --kategoria Jedzenie --data-od 2024-01-01` |
| `edytuj` | Edit an expense | `python -m tracker.main edytuj -i 3 -k 18.99` |
| `usun` | Delete an expense | `python -m tracker.main usun -i 4` |
| `podsumowanie` | Expense summary/statistics | `python -m tracker.main podsumowanie --rok 2024 --miesiac 06` |
| `raport` | Full monthly report | `python -m tracker.main raport -r 2024 -m 06` |

### Recurring Expenses (`cykliczne`)

Managed under the `cykliczne` subcommand:

| Subcommand | Description | Example |
|---|---|---|
| `dodaj` | Add a recurring expense | `python -m tracker.main cykliczne dodaj -o "Netflix" -k 50 --czestotliwosc Miesięczne` |
| `wypisz` | List recurring expenses | `python -m tracker.main cykliczne wypisz` |
| `edytuj` | Edit a recurring expense | `python -m tracker.main cykliczne edytuj -i 1 -k 60` |
| `usun` | Delete a recurring expense | `python -m tracker.main cykliczne usun -i 1` |

Recurring expenses are automatically synced to the main expense list on each run.

Available frequencies: `Codzienne`, `Tygodniowe`, `Dwutygodniowe`, `Miesięczne`, `Roczne`

### Budget (`budzet`)

Managed under the `budzet` subcommand:

| Subcommand | Description | Example |
|---|---|---|
| `ustaw` | Set a budget | `python -m tracker.main budzet ustaw -k 2000 --od 2024-01` |
| `wylacz` | Disable budget | `python -m tracker.main budzet wylacz --od 2024-06` |
| `aktualny` | Show current active budget | `python -m tracker.main budzet aktualny` |
| `wypisz` | List all budget entries | `python -m tracker.main budzet wypisz` |
| `raport` | Budget report for a month | `python -m tracker.main budzet raport --data 2024-06` |
| `usun` | Delete a budget entry | `python -m tracker.main budzet usun -i 2` |

Use `--tylko-ten` with `ustaw` or `wylacz` to apply the change only to the current month.

### Export (`eksport`)

Managed under the `eksport` subcommand:

| Subcommand | Description | Example |
|---|---|---|
| `wydatki` | Export expenses | `python -m tracker.main eksport wydatki --format xlsx --plik expenses` |
| `cykliczne` | Export recurring expenses | `python -m tracker.main eksport cykliczne --format json --plik recurring` |
| `budzet` | Export budget data | `python -m tracker.main eksport budzet --format csv --plik budget` |

Supported formats: `csv`, `json`, `xlsx`. Files are saved to the `exports/` directory by default, or to any path you specify.

For budget export, use `--tryb ustawienia` (raw settings) or `--tryb obowiazujace` (expanded month-by-month).

---

## Common Filters

Most list and export commands support these filters:

| Flag | Description |
|---|---|
| `--data-od` / `--data-do` | Date range (YYYY-MM-DD) |
| `--kwota-od` / `--kwota-do` | Amount range |
| `--kategoria` | Filter by category |
| `--sortuj-po` | Sort by field |
| `--malejaco` | Sort descending |

---

## Categories

`Jedzenie`, `Zakupy`, `Transport`, `Rozrywka`, `Zdrowie`, `Inne`

---

## GUI Features

The GUI (PyQt6) currently supports:

* Viewing, filtering and sorting expenses
* Adding new expenses
* Editing and deleting expenses (including via double-click in the table)
* Viewing, filtering recurring expenses
* Adding new recurring expenses
* Editing and deleting recurring expenses

---

## Project Structure
```
.
├── tracker/
│   ├── __init__.py
│   ├── main.py           # CLI entry point
│   ├── commands.py       # Business logic
│   ├── file_ops.py       # CSV/file operations
│   ├── validators.py     # Input validation (CLI)
│   ├── data_validation.py # Data integrity checks
│   └── utils.py          # Filtering, sorting, statistics
├── gui/
│   ├── __init__.py
│   ├── app.py            # GUI entry point
│   ├── main_window.py    # Main window & navigation
│   ├── custom_items.py   # Custom table widgets
│   └── views/
│       ├── expenses_view.py
│       ├── add_expense_view.py
│       ├── edit_expense_view.py
│       ├── recurring_view.py
│       ├── add_recurring_view.py
│       └── edit_recurring_view.py
├── main_gui.py           # GUI launcher
├── wydatki.csv           # Expense data (not committed)
├── recurring.csv         # Recurring expense data (not committed)
├── budget.csv            # Budget data (not committed)
├── README.md
└── .gitignore
```

---

## Data & Backups
* Data is stored in wydatki.csv, recurring.csv and budget.csv in the project root
* Automatic backups are created before every write operation (up to 20 kept per file, stored in backups/)
* Emergency backups are created when file format issues are detected (emergency backups/)
* None of the data files or backup directories are tracked by git

---

## Requirements
* Python 3.7+
* tabulate
* openpyxl
* python-dateutil
* PyQt6 (GUI only)

---

## Quick Start
```
git clone https://github.com/Leprex24/expenses-tracker-python.git
cd expense-tracker

# Optional: virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt

# Run CLI
python -m tracker.main dodaj -o "Coffee" -k 12 --kategoria Jedzenie

# Run GUI
python main_gui.py
```
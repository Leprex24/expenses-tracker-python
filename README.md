# Expense Tracker
A simple command-line Python application for tracking personal expenses. Written for educational and personal budgeting purposes.

## Features

* Add new expenses with category, amount, and description
* List/filter/sort your expenses
* Edit or delete entries
* Summarize expenses by category or date range
* Data stored in a local CSV file

### Quick Start

#### 1. Clone the Repo and Set Up

```
git clone https://github.com/Leprex24/expenses-tracker-python.git
cd expense-tracker
(Optional) Set up a virtualenv:
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```
#### 2. Run the Program
From your project root:
```
python -m tracker.main [command] [options]
```
Examples:
```
python -m tracker.main dodaj -o "Pizza" -k 30 --kategoria Jedzenie
python -m tracker.main wypisz
python -m tracker.main podsumowanie --rok 2024 --miesiac 06
```

### Commands
| Command      | Description	       | Usage Example                                   |
|--------------|--------------------|-------------------------------------------------| 
| dodaj	       | Add an expense     | python -m tracker.main dodaj -o "chleb" -k 7.50 |
| wypisz       | List expenses      | python -m tracker.main wypisz                   |
| podsumowanie | Summarize expenses | python -m tracker.main podsumowanie --rok 2024  |
| edytuj       | Edit an expense    | python -m tracker.main edytuj -i 3 -k 18.99     |
| usun         | Delete an expense  | python -m tracker.main usun -i 4                |

### Categories
Supported categories:

* Jedzenie (Food)
* Zakupy (Shopping)
* Transport (Transportation)
* Rozrywka (Entertainment)
* Inne (Other)

### Requirements

* Python 3.7+
* tabulate

### Data Storage

* All expenses are saved to a CSV file called wydatki.csv in your project root.
* This file is not tracked by git (see .gitignore). Make your own backups if needed.

### Project Structure
```
.
├── tracker/
│   ├── __init__.py
│   ├── main.py
│   ├── file_ops.py
│   ├── validators.py
│   ├── commands.py
│   └── utils.py
├── wydatki.csv        # data file, not committed
├── README.md
├── .gitignore
└── .venv/             # optional, your virtual environment
```

### Contributing
Pull requests and suggestions are welcome! Please open an issue or PR.

### License
MIT License
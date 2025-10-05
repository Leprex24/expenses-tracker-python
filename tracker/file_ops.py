import csv
import os
import shutil
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, 'wydatki.csv')
RECURRING_PATH = os.path.join(PROJECT_ROOT, 'recurring.csv')
BACKUP_PATH = os.path.join(PROJECT_ROOT, 'backups')
BUDGET_PATH = os.path.join(PROJECT_ROOT, 'budget.csv')

def file_verification_main():
    if not os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
        print(f"Utworzono nowy plik: {CSV_PATH}")
    else:
        with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
        expected_columns = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria']
        if header == expected_columns:
            print(f"Plik {CSV_PATH} już istnieje w poprawnym formacie")
        else:
            override = int(input(f"Plik {CSV_PATH} już istnieje, ale w innym formacie, czy chcesz go nadpisać? Podaj 1 dla tak lub 0 dla nie: "))
            while override != 1 and override != 0:
                override = int(input("Podano złą wartość spróbuj jeszcze raz:"))
            if override == 1:
                with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
                print(f"Nadpisano plik: {CSV_PATH}")

def get_all_expenses_main():
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)

def write_all_expenses_main(all_rows):
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
        writer.writerows(all_rows)

def add_new_expense_main(expense_id, date, description, amount, category):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([expense_id, date, description, amount, category])

def create_backup():
    os.makedirs(BACKUP_PATH, exist_ok=True)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"wydatki_backup_{timestamp}.csv"
    backup_fullpath = os.path.join(BACKUP_PATH, backup_filename)
    shutil.copyfile(CSV_PATH, backup_fullpath)
    print(f"Utworzono kopie zapasową: {backup_fullpath}")
    delete_old_backups()

def delete_old_backups():
    backups = [f for f in os.listdir(BACKUP_PATH) if f.startswith("wydatki_backup") and f.endswith(".csv")]
    if len(backups) > 20:
        backups.sort()
        num_to_delete = len(backups) - 20
        for old_backup in backups[:num_to_delete]:
            backup_for_removal = os.path.join(BACKUP_PATH, old_backup)
            os.remove(backup_for_removal)

def file_verification_recurring():
    if not os.path.exists(RECURRING_PATH):
        with open(RECURRING_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość'])
        print(f"Utworzono nowy plik: {RECURRING_PATH}")
    else:
        with open(RECURRING_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
        expected_columns = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość']
        if header == expected_columns:
            print(f"Plik {RECURRING_PATH} już istnieje w poprawnym formacie")
        else:
            override = int(input(f"Plik {RECURRING_PATH} już istnieje, ale w innym formacie, czy chcesz go nadpisać? Podaj 1 dla tak lub 0 dla nie: "))
            while override != 1 and override != 0:
                override = int(input("Podano złą wartość spróbuj jeszcze raz:"))
            if override == 1:
                with open(RECURRING_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość'])
                print(f"Nadpisano plik: {RECURRING_PATH}")

def load_recurring_expenses():
    with open(RECURRING_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)

def add_new_recurring_expense(expense_id, date, description, amount, category, frequency):
    with open(RECURRING_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([expense_id, date, description, amount, category, frequency])

def write_all_recurring_expenses(all_rows):
    with open(RECURRING_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość'])
        writer.writerows(all_rows)

def file_verification_budget():
    if not os.path.exists(BUDGET_PATH):
        with open(BUDGET_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status'])
        print(f"Utworzono nowy plik: {BUDGET_PATH}")
    else:
        with open(BUDGET_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
        expected_columns = ['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status']
        if header == expected_columns:
            print(f"Plik {BUDGET_PATH} już istnieje w poprawnym formacie")
        else:
            override = int(input(f"Plik {BUDGET_PATH} już istnieje, ale w innym formacie, czy chcesz go nadpisać? Podaj 1 dla tak lub 0 dla nie: "))
            while override != 1 and override != 0:
                override = int(input("Podano złą wartość spróbuj jeszcze raz:"))
            if override == 1:
                with open(BUDGET_PATH, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status'])
                print(f"Nadpisano plik: {BUDGET_PATH}")

def load_budgets():
    with open(BUDGET_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)

def add_budget(id, year, month, amount):
    with open(BUDGET_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([id, year, month, amount])

def write_all_budgets(all_rows):
    all_rows.sort(key=lambda row: (int(row[1]), int(row[2])))
    with open(BUDGET_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status'])
        writer.writerows(all_rows)
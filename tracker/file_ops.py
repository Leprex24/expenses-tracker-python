import csv
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, 'wydatki.csv')

def file_verification():
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

def get_all_expenses():
    with open(CSV_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        return list(reader)

def write_all_expenses(all_rows):
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
        writer.writerows(all_rows)

def add_new_expense(expense_id, date, description, amount, category):
    with open(CSV_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([expense_id, date, description, amount, category])
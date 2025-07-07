import argparse
import datetime
import csv
import tabulate
import os

def file_verification(file_name='wydatki.csv'):
    if not os.path.exists(file_name):
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
        print(f"Utworzono nowy plik: {file_name}")
    else:
        with open(file_name, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            expected_columns = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria']
            if header == expected_columns:
                print(f"Plik {file_name} juz istnieje w poprawnym formacie")
            else:
                override = int(input(f"Plik {file_name} juz istnieje ale w innym formacie, czy chcesz go nadpisac? Podaj 1 dla tak lub 0 dla nie: "))
                while override != 1 and override != 0:
                    override = int(input("Podana zla wartosc sprobuj jeszcze raz:"))
                if override == 1:
                    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
                    print(f"Nadpisano plik: {file_name}")

def add_expense(args):
    ID = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria

    if ID == None:
        with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            ID_list = [int(row[0]) for row in reader if row[0] != 'ID']
            ID = max(ID_list, default=0)+1

    if date == None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category == None:
        category = "Zakupy"

    with open('wydatki.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ID, date, description, amount, category])

    print(f"Dodano nowy wydatek (ID: {ID})")

def list_expenses(args):
    category = args.kategoria
    sum = 0
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
    data = []
    if not all_rows:
        print("Nie dodano jeszcze zadnych wydatkow")
        return

    if category == None:
        data = all_rows
    else:
        data = [row for row in all_rows if row[4] == category]

    for row in data:
        sum += float(row[3])

    if data:
        print(tabulate.tabulate(data, headers=['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'], tablefmt="github"))
        print(f"Suma: {sum:.2f} zl")
    else:
        print("Brak wydatków do wyswietlenia")

def delete_expense(args):
    ID = args.id
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        ID_list = [int(row[0]) for row in all_rows]
    if ID not in ID_list:
        print(f"Nie mozna usunac wydatku o ID: {ID}, poniewaz takowy nie istnieje!")
    else:
        all_rows = [row for row in all_rows if int(row[0]) != ID]
        with open('wydatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
            writer.writerows(all_rows)
        print(f"Usunieto wydatek (ID: {ID})")



def main():
    file_verification()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode', help='Dostepne tryby')

    add_parser = subparsers.add_parser('dodaj', help='Dodaj nowy wydatek')
    add_parser.add_argument('-o', '--opis', type=str, required=True ,help='Opis wydatku')
    add_parser.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    add_parser.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyslnie data dzisiejsza')
    add_parser.add_argument('--id', help='Niestandardowe ID')
    add_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Kategoria wydatku, domyslnie zakupy')

    list_parser = subparsers.add_parser('wypisz', help='Wypisz wszystkie wydatki')
    list_parser.add_argument('-k', '--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka' ], help='Kategoria wydatku')

    delete_parser = subparsers.add_parser('usun', help='Usun istniejacy wydatek')
    delete_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do usuniecia')

    args = parser.parse_args()

    if args.mode == 'dodaj':
        add_expense(args)

    if args.mode == 'wypisz':
        list_expenses(args)

    if args.mode == 'usun':
        delete_expense(args)

    if not args.mode:
        parser.print_help()

if __name__ == '__main__':
    main()
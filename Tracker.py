import argparse
import datetime
import csv
from operator import index

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
                print(f"Plik {file_name} już istnieje w poprawnym formacie")
            else:
                override = int(input(f"Plik {file_name} już istnieje, ale w innym formacie, czy chcesz go nadpisać? Podaj 1 dla tak lub 0 dla nie: "))
                while override != 1 and override != 0:
                    override = int(input("Podano złą wartość spróbuj jeszcze raz:"))
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

def filter_by_date(args, all_rows):
    date = args.data
    date_from = args.data_od
    date_to = args.data_do

    if date != None:
        data = [row for row in all_rows if row[1] == date]

    if date_from == None and date_to == None:
        data = all_rows
    elif date_from == None and date_to != None:
        data = [row for row in all_rows if row[1] <= date_to]
    elif date_from != None and date_to == None:
        data = [row for row in all_rows if row[1] >= date_from]
    else:
        data = [row for row in all_rows if row[1] >= date_from and row[1] <= date_to]

    return data

def list_expenses(args):
    if args.data and args.data_od:
        print("Błąd: --data nie może być używana z --data-od")
        return
    if args.data and args.data_do:
        print("Błąd: --data nie może być używana z --data-do")
        return
    if args.data_do and args.data_od and args.data_do < args.data_od:
        print("Błąd: --data-do nie może być wcześniejsza niż --data-od")
        return

    category = args.kategoria
    sum = 0
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
    if not all_rows:
        print("Nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_date(args, all_rows)

    if category != None:
        data = [row for row in data if row[4] == category]

    for row in data:
        sum += float(row[3])

    if data:
        print(tabulate.tabulate(data, headers=['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'], tablefmt="github"))
        print(f"Suma: {sum:.2f} zł")
    else:
        print("Brak wydatków do wyświetlenia")

def delete_expense(args):
    ID = args.id
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        ID_list = [int(row[0]) for row in all_rows]
    if ID not in ID_list:
        print(f"Nie można usunać wydatku o ID: {ID}, ponieważ takowy nie istnieje!")
    else:
        all_rows = [row for row in all_rows if int(row[0]) != ID]
        with open('wydatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
            writer.writerows(all_rows)
        print(f"Usunięto wydatek (ID: {ID})")

def edit_expense(args):
    ID = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        ID_list = [int(row[0]) for row in all_rows]
    if ID not in ID_list:
        print(f"Nie można edytowac wydatku o ID: {ID}, ponieważ takowy nie istnieje!")
    else:
        row_index = ID_list.index(ID)
        if date != None:
            all_rows[row_index][1] = date
        if description != None:
            all_rows[row_index][2] = description
        if amount != None:
            all_rows[row_index][3] = amount
        if category != None:
            all_rows[row_index][4] = category
        with open('wydatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
            writer.writerows(all_rows)
        print(f"Edytowano wydatek (ID: {ID})")


def main():
    file_verification()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode', help='Dostepne tryby')

    add_parser = subparsers.add_parser('dodaj', help='Dodaj nowy wydatek')
    add_parser.add_argument('-o', '--opis', type=str, required=True ,help='Opis wydatku')
    add_parser.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    add_parser.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyślnie data dzisiejsza')
    add_parser.add_argument('--id', help='Niestandardowe ID')
    add_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Kategoria wydatku, domyślnie zakupy')

    list_parser = subparsers.add_parser('wypisz', help='Wypisz wszystkie wydatki')
    list_parser.add_argument('-k', '--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka' ], help='Kategoria wydatku')
    list_parser.add_argument('--data-od', help='Data początkowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data-do', help='Data końcowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data', help='Konkretna data wyświetlanych wydatków (YYYY-MM-DD)')

    delete_parser = subparsers.add_parser('usun', help='Usuń istniejący wydatek')
    delete_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do usunięcia')

    edit_parser = subparsers.add_parser('edytuj', help='Edytuj wydatek')
    edit_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do edycji')
    edit_parser.add_argument('-o', '--opis', type=str, help='Nowy opis wydatku')
    edit_parser.add_argument('-k', '--kwota', type=float, help='Nowa kwota wydatku')
    edit_parser.add_argument('-d', '--data', help='Nowa data wydatku (YYYY-MM-DD)')
    edit_parser.add_argument('--kategoria', help='Nowa kategoria wydatku')

    args = parser.parse_args()

    if args.mode == 'dodaj':
        add_expense(args)

    if args.mode == 'wypisz':
        list_expenses(args)

    if args.mode == 'usun':
        delete_expense(args)

    if args.mode == 'edytuj':
        edit_expense(args)

    if not args.mode:
        parser.print_help()

if __name__ == '__main__':
    main()
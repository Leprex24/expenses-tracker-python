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
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria

    if expense_id is None:
        with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            id_list = [int(row[0]) for row in reader if row[0] != 'ID']
            expense_id = max(id_list, default=0)+1

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category is None:
        category = "Zakupy"

    with open('wydatki.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([expense_id, date, description, amount, category])

    print(f"Dodano nowy wydatek (ID: {expense_id})")

def filter_by_date(args, all_rows):
    date_from = args.data_od
    date_to = args.data_do

    if date_from is None and date_to is None:
        data = all_rows
    elif date_from is None and date_to is not None:
        data = [row for row in all_rows if row[1] <= date_to]
    elif date_from is not None and date_to is None:
        data = [row for row in all_rows if row[1] >= date_from]
    else:
        data = [row for row in all_rows if date_from <= row[1] <= date_to]
    if args.mode == "wypisz":
        date = args.data
        if date is not None:
            data = [row for row in all_rows if row[1] == date]
    return data

def sort_expenses(data, sort_by, reverse):
    key_map = {
        'ID': lambda x: int(x[0]),
        'Data': lambda x: x[1],
        'Kwota': lambda x: float(x[3]),
        'Kategoria': lambda x: x[4]
    }
    data.sort(key=key_map[sort_by], reverse=reverse)
    return data

def list_expenses(args):
    category = args.kategoria
    sort_by = args.sortuj_po
    reverse = args.malejaco
    sum_of_expenses = 0
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
    if not all_rows:
        print("Nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_date(args, all_rows)

    if category is not None:
        data = [row for row in data if row[4] == category]

    data = sort_expenses(data, sort_by, reverse)

    for row in data:
        sum_of_expenses += float(row[3])

    if data:
        print(tabulate.tabulate(data, headers=['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'], tablefmt="github", numalign="center"))
        print(f"Suma: {sum_of_expenses:.2f} zł")
    else:
        print("Brak wydatków do wyświetlenia")

def delete_expense(args):
    expense_id = args.id
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        id_list = [int(row[0]) for row in all_rows]
    if expense_id not in id_list:
        print(f"Nie można usunać wydatku o ID: {expense_id}, ponieważ takowy nie istnieje!")
    else:
        all_rows = [row for row in all_rows if int(row[0]) != expense_id]
        with open('wydatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
            writer.writerows(all_rows)
        print(f"Usunięto wydatek (ID: {expense_id})")

def edit_expense(args):
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
        id_list = [int(row[0]) for row in all_rows]
    if expense_id not in id_list:
        print(f"Nie można edytowac wydatku o ID: {expense_id}, ponieważ takowy nie istnieje!")
    else:
        row_index = id_list.index(expense_id)
        if date is not None:
            all_rows[row_index][1] = date
        if description is not None:
            all_rows[row_index][2] = description
        if amount is not None:
            all_rows[row_index][3] = amount
        if category is not None:
            all_rows[row_index][4] = category
        with open('wydatki.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
            writer.writerows(all_rows)
        print(f"Edytowano wydatek (ID: {expense_id})")

def calculate_expense_stats(data, category=None):
    sum_of_expenses = 0
    if category is not None:
        data = [row for row in data if row[4] == category]
    number_of_expenses = len(data)
    if number_of_expenses == 0:
        sum_of_expenses = 0
        average_expense = 0
        highest_expense = 0
        lowest_expense = 0
    else:
        for row in data:
            sum_of_expenses += float(row[3])
        average_expense = round(sum_of_expenses / number_of_expenses,2)
        highest_expense = max(float(row[3]) for row in data)
        lowest_expense = min(float(row[3]) for row in data)
    statistics = [
        number_of_expenses,
        sum_of_expenses,
        average_expense,
        highest_expense,
        lowest_expense
    ]
    return statistics

def refine_statistics(statistics, category):
    statistics.pop()
    statistics.pop()
    statistics.insert(0, category)
    return statistics

def summarize_expenses(args):
    category = args.kategoria
    month = args.miesiac
    year = args.rok

    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        all_rows = list(reader)
    if not all_rows:
        print("Nie można pokazać podsumowania, ponieważ nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_date(args, all_rows)

    if month is not None:
        data = [row for row in all_rows if row[1].startswith(year + "-" + month)]
    elif year is not None:
        data = [row for row in all_rows if row[1].startswith(year)]

    if data:
        if category is None:
            overall_statistics = calculate_expense_stats(data)
            print("1. Ogólne informacje:")
            print(f"\u2022 Całkowita liczba wydatków: {overall_statistics[0]}")
            print(f"\u2022 Suma wszystkich wydatków: {overall_statistics[1]:.2f} zł")
            print(f"\u2022 Średni wydatek: {overall_statistics[2]:.2f} zł")
            print(f"\u2022 Najwyższy wydatek: {overall_statistics[3]:.2f} zł")
            print(f"\u2022 Najniższy wydatek: {overall_statistics[4]:.2f} zł")
            statistics_food = refine_statistics(calculate_expense_stats(data, "Jedzenie"), "Jedzenie")
            statistics_shopping = refine_statistics(calculate_expense_stats(data, "Zakupy"), "Zakupy")
            statistics_transport = refine_statistics(calculate_expense_stats(data, "Transport"), "Transport")
            statistics_entertainment = refine_statistics(calculate_expense_stats(data, "Rozrywka"), "Rozrywka")
            statistics_other = refine_statistics(calculate_expense_stats(data, "Inne"), "Inne")
            category_statistics = [
                statistics_food,
                statistics_shopping,
                statistics_transport,
                statistics_entertainment,
                statistics_other,
            ]
            print("2. Podsumowanie po kategoriach:")
            print(tabulate.tabulate(category_statistics, headers=["Kategoria", "Wydatki", "Suma", "Średnia"], tablefmt="github", numalign="center"))
        else:
            statistics_filter_category = calculate_expense_stats(data, category)
            print(f"Ogólne informacje dla kategorii {category}:")
            print(f"\u2022 Całkowita liczba wydatków: {statistics_filter_category[0]}")
            print(f"\u2022 Suma wszystkich wydatków: {statistics_filter_category[1]:.2f} zł")
            print(f"\u2022 Średni wydatek: {statistics_filter_category[2]:.2f} zł")
            print(f"\u2022 Najwyższy wydatek: {statistics_filter_category[3]:.2f} zł")
            print(f"\u2022 Najniższy wydatek: {statistics_filter_category[4]:.2f} zł")
    else:
        print("Brak wydatków w podanym okresie czasowym")

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
    list_parser.add_argument('-k', '--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka' ], help='Kategoria wydatków')
    list_parser.add_argument('--data-od', help='Data początkowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data-do', help='Data końcowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data', help='Konkretna data wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('-s', '--sortuj-po', choices=['ID', 'Data', 'Kwota', 'Kategoria'], help='Sortowanie wydatków, domuślnie ID', default='ID')
    list_parser.add_argument('--malejaco', action='store_true', help='Sortuj malejąco, domyślnie rosnąco')

    delete_parser = subparsers.add_parser('usun', help='Usuń istniejący wydatek')
    delete_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do usunięcia')

    edit_parser = subparsers.add_parser('edytuj', help='Edytuj wydatek')
    edit_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do edycji')
    edit_parser.add_argument('-o', '--opis', type=str, help='Nowy opis wydatku')
    edit_parser.add_argument('-k', '--kwota', type=float, help='Nowa kwota wydatku')
    edit_parser.add_argument('-d', '--data', help='Nowa data wydatku (YYYY-MM-DD)')
    edit_parser.add_argument('--kategoria', help='Nowa kategoria wydatku')

    summary_parser = subparsers.add_parser('podsumowanie', help='Podsumowanie wydatków')
    summary_parser.add_argument('-k' ,'--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka'], help='Kategoria wydatków do podsumowania')
    summary_parser.add_argument('-m', '--miesiac', type=str, help='Miesiac wydatków do podsumowania (MM)')
    summary_parser.add_argument('-r', '--rok', type=str, help='Rok wydatków do podsumowania (YYYY)')
    summary_parser.add_argument('--data-od', help='Data początkowa wydatków do podsumowania (YYYY-MM-DD)')
    summary_parser.add_argument('--data-do', help='Data końcowa wydatków do podsumowania (YYYY-MM-DD)')

    args = parser.parse_args()

    if args.mode == 'dodaj':
        add_expense(args)

    if args.mode == 'wypisz':
        if args.data and args.data_od:
            parser.error("--data nie może być używana z --data-od")
        elif args.data and args.data_do:
            parser.error("--data nie może być używana z --data-do")
        elif args.data_do and args.data_od and args.data_do < args.data_od:
            parser.error("--data-do nie może być wcześniejsza niż --data-od")
        else:
            list_expenses(args)

    if args.mode == 'usun':
        delete_expense(args)

    if args.mode == 'edytuj':
        edit_expense(args)

    if args.mode == 'podsumowanie':
        if args.miesiac and not args.rok:
            parser.error("Aby wyświetlić podsumowanie konkretnego miesiąca musisz podać --rok")
        elif args.data_do and args.data_od and args.data_do < args.data_od:
            parser.error("--data-do nie może być wcześniejsza niż --data-od")
        elif (args.miesiac or args.rok) and (args.data_od or args.data_do):
            parser.error("--miesiac i --rok nie mogą być używane jednocześnie z --data-od i --data-do")
        else:
            summarize_expenses(args)


    if not args.mode:
        parser.print_help()

if __name__ == '__main__':
    main()
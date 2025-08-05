import datetime
import tabulate

from tracker.file_ops import get_all_expenses, write_all_expenses, add_new_expense, create_backup
from tracker.utils import filter_by_date, sort_expenses, calculate_expense_stats, refine_statistics

def add_expense(args):
    create_backup()
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria

    if expense_id is None:
        all_expenses = get_all_expenses()
        id_list = [int(row[0]) for row in all_expenses if row[0] != 'ID']
        expense_id = max(id_list, default=0)+1

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category is None:
        category = "Zakupy"

    add_new_expense(expense_id, date, description, amount, category)

    print(f"Dodano nowy wydatek (ID: {expense_id})")

def list_expenses(args):
    category = args.kategoria
    sort_by = args.sortuj_po
    reverse = args.malejaco
    sum_of_expenses = 0
    all_rows = get_all_expenses()
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
    create_backup()
    expense_id = args.id
    all_rows = get_all_expenses()
    all_rows = [row for row in all_rows if int(row[0]) != expense_id]
    write_all_expenses(all_rows)
    print(f"Usunięto wydatek (ID: {expense_id})")

def edit_expense(args):
    create_backup()
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    all_rows = get_all_expenses()
    id_list = [int(row[0]) for row in all_rows]
    row_index = id_list.index(expense_id)
    if date is not None:
        all_rows[row_index][1] = date
    if description is not None:
        all_rows[row_index][2] = description
    if amount is not None:
        all_rows[row_index][3] = amount
    if category is not None:
        all_rows[row_index][4] = category
    write_all_expenses(all_rows)
    print(f"Edytowano wydatek (ID: {expense_id})")

def summarize_expenses(args):
    category = args.kategoria
    month = args.miesiac
    year = args.rok

    all_rows = get_all_expenses()
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

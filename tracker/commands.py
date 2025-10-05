import datetime
import tabulate

from tracker.file_ops import get_all_expenses_main, write_all_expenses_main, add_new_expense_main, create_backup, \
    add_new_recurring_expense, load_recurring_expenses, write_all_recurring_expenses, load_budgets, write_all_budgets
from tracker.utils import filter_by_date, sort_expenses, calculate_expense_stats, refine_statistics, get_due_dates, \
    find_last_due_date, date_to_string, already_exists, filter_by_amount, normalize_year_month


def add_expense(args):
    create_backup()
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria

    if expense_id is None:
        all_expenses = get_all_expenses_main()
        id_list = [int(row[0]) for row in all_expenses if row[0] != 'ID']
        expense_id = max(id_list, default=0)+1

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category is None:
        category = "Zakupy"

    add_new_expense_main(expense_id, date, description, amount, category)

    print(f"Dodano nowy wydatek (ID: {expense_id})")

def list_expenses(args):
    category = args.kategoria
    sort_by = args.sortuj_po
    reverse = args.malejaco
    sum_of_expenses = 0
    all_rows = get_all_expenses_main()
    if not all_rows:
        print("Nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_date(args, all_rows)
    data = filter_by_amount(args, data)
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
    all_rows = get_all_expenses_main()
    all_rows = [row for row in all_rows if int(row[0]) != expense_id]
    write_all_expenses_main(all_rows)
    print(f"Usunięto wydatek (ID: {expense_id})")

def edit_expense(args):
    create_backup()
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    all_rows = get_all_expenses_main()
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
    write_all_expenses_main(all_rows)
    print(f"Edytowano wydatek (ID: {expense_id})")

def summarize_expenses(args):
    category = args.kategoria
    month = args.miesiac
    year = args.rok

    all_rows = get_all_expenses_main()
    if not all_rows:
        print("Nie można pokazać podsumowania, ponieważ nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_date(args, all_rows)
    data = filter_by_amount(args, data)

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

def add_recurring_expense(args):
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    frequency = args.czestotliwosc

    if expense_id is None:
        all_expenses = load_recurring_expenses()
        id_list = [int(row[0]) for row in all_expenses if row[0] != 'ID']
        expense_id = max(id_list, default=0) + 1

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category is None:
        category = "Zakupy"

    add_new_recurring_expense(expense_id, date, description, amount, category, frequency)

    print(f"Dodano nowy wydatek (ID: {expense_id})")

def list_recurring_expenses(args):
    category = args.kategoria
    sort_by = args.sortuj_po
    reverse = args.malejaco
    frequency = args.czestotliwosc
    sum_of_expenses = 0
    all_rows = load_recurring_expenses()
    if not all_rows:
        print("Nie dodano jeszcze żadnych wydatków")
        return
    data = filter_by_amount(args, all_rows)

    if category is not None:
        data = [row for row in data if row[4] == category]

    if frequency is not None:
        data = [row for row in data if row[5] == frequency]

    data = sort_expenses(data, sort_by, reverse)

    for row in data:
        sum_of_expenses += float(row[3])

    if data:
        print(tabulate.tabulate(data, headers=['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość'], tablefmt="github", numalign="center"))
        print(f"Suma: {sum_of_expenses:.2f} zł")
    else:
        print("Brak wydatków do wyświetlenia")

def delete_recurring_expense(args):
    expense_id = args.id
    all_rows = load_recurring_expenses()
    all_rows = [row for row in all_rows if int(row[0]) != expense_id]
    write_all_recurring_expenses(all_rows)
    print(f"Usunięto wydatek (ID: {expense_id})")

def edit_recurring_expense(args):
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = args.kwota
    category = args.kategoria
    frequency = args.czestotliwosc
    all_rows = load_recurring_expenses()
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
    if frequency is not None:
        all_rows[row_index][5] = frequency
    write_all_recurring_expenses(all_rows)
    print(f"Edytowano wydatek (ID: {expense_id})")

def sync_recurring_expenses():
    recurring_templates = load_recurring_expenses()
    all_expenses = get_all_expenses_main()
    id_list = [int(row[0]) for row in all_expenses if row[0] != 'ID']
    expense_id = max(id_list, default=0) + 1
    for rec in recurring_templates:
        next_dates = get_due_dates(find_last_due_date(rec, all_expenses), rec[5], datetime.date.today())
        for date in next_dates:
            date_str = date_to_string(date)
            if not already_exists(rec, date_str, all_expenses):
                add_new_expense_main(expense_id, date_str, rec[2], rec[3], rec[4])
                expense_id += 1

def set_budget(args):
    all_budgets = load_budgets()
    amount = args.kwota
    id_list = [int(row[0]) for row in all_budgets if row[0] != 'ID']
    budget_id = max(id_list, default=0) + 1
    one_off = args.tylko_ten
    if one_off:
        status = "CURRENT"
    else:
        status = "ON"
    if args.od:
        year, month = normalize_year_month(args.od)
    else:
        today = datetime.date.today()
        year = f"{today.year:04d}"
        month = f"{today.month:02d}"
    provided_date_index = next((i for i, row in enumerate(all_budgets) if row[1] == year and row[2] == month), None)
    if provided_date_index is not None:
        all_budgets[provided_date_index][3] = amount
        all_budgets[provided_date_index][4] = status
    else:
        all_budgets.append([budget_id, year, month, amount, status])
    write_all_budgets(all_budgets)


def remove_budget(args):
    budget_id = args.id
    all_budgets = load_budgets()
    all_budgets = [row for row in all_budgets if int(row[0]) != budget_id]
    write_all_budgets(all_budgets)
    print(f"Usunięto budżet o ID: {budget_id}")

def current_budget():
    all_budgets = load_budgets()
    if not all_budgets:
        print("Aktualnie nie obowiązuje żaden budżet")
        return
    else:
        today = datetime.date.today()
        current_year, current_month = f"{today.year:04d}", f"{today.month:02d}"
        exact_current = next((row for row in all_budgets if row[1] == current_year and row[2] == current_year and row[4] == "CURRENT"), None)
        if exact_current:
            if exact_current[3]:
                print(f"Aktualny budżet wynosi {float(exact_current[3]):.2f} zł na miesiąc (tylko ten miesiąc)")
            else:
                print("W tym miesiącu budżet jest wyłączony (tylko ten miesiąc)")
            return
        last_change = next((row for row in reversed(all_budgets) if (row[1], row[2]) <= (current_year, current_month) and row[4] in ("ON", "OFF")), None)
        if not last_change:
            print("Aktualnie nie obowiązuje żaden budżet")
            return
        if last_change[4] == "ON":
            print(f"Aktualny budżet wynosi {float(last_change[3]):.2f} zł na miesiąc i obowiązuje od {last_change[1]}-{last_change[2]}")
        else:
            print(f"Aktualnie nie obowiązuje żaden budżet (wyłączony od {last_change[1]}-{last_change[2]})")
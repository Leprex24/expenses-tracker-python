import datetime
from calendar import monthrange, month_name

import tabulate

from tracker.file_ops import get_all_expenses_main, write_all_expenses_main, add_new_expense_main, create_backup, \
    add_new_recurring_expense, load_recurring_expenses, write_all_recurring_expenses, load_budgets, write_all_budgets, \
    CSV_PATH, RECURRING_PATH, BUDGET_PATH, resolve_export_path, export_to_csv, export_to_json, create_emergency_backup, \
    export_to_excel
from tracker.utils import filter_by_date, sort_expenses, calculate_expense_stats, refine_statistics, get_due_dates, \
    find_last_due_date, date_to_string, already_exists, filter_by_amount, normalize_year_month, sort_budgets, \
    sum_expenses_in_month, filter_by_date_budgets, filter_by_amount_budgets, create_expenses_metadata, \
    expand_budgets_to_months, print_budget_section, print_expenses_section, print_recurring_section, print_top_expenses

MONTH_NAMES = {
    1: "Styczeń",
    2: "Luty",
    3: "Marzec",
    4: "Kwiecień",
    5: "Maj",
    6: "Czerwiec",
    7: "Lipiec",
    8: "Sierpień",
    9: "Wrzesień",
    10: "Październik",
    11: "Listopad",
    12: "Grudzień"
}


def add_expense(description, amount, date=None, category=None, expense_id=None):
    create_backup(CSV_PATH)
    amount = f"{float(amount):.2f}"

    if expense_id is None:
        all_expenses = get_all_expenses_main()
        id_list = [int(row[0]) for row in all_expenses if row[0] != 'ID']
        expense_id = max(id_list, default=0)+1

    if date is None:
        date = datetime.datetime.now().strftime("%Y-%m-%d")

    if category is None:
        category = "Zakupy"

    add_new_expense_main(expense_id, date, description, amount, category)

    return expense_id

def list_expenses(args):
    category = args.kategoria
    sort_by = args.sortuj_po
    reverse = args.malejaco
    sum_of_expenses = 0
    all_rows = get_all_expenses_main()
    if not all_rows:
        print("Nie dodano jeszcze żadnych wydatków")
        return
    date_from = args.data_od
    date_to = args.data_do
    data = filter_by_date(date_from, date_to, all_rows, args)
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    data = filter_by_amount(amount_from, amount_to, data)
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
    create_backup(CSV_PATH)
    expense_id = args.id
    all_rows = get_all_expenses_main()
    all_rows = [row for row in all_rows if int(row[0]) != expense_id]
    write_all_expenses_main(all_rows)
    print(f"Usunięto wydatek (ID: {expense_id})")

def edit_expense(description, amount, date, expense_id, category):
    create_backup(CSV_PATH)
    amount_str = f"{float(amount):.2f}" if amount is not None else None
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
    return True

def summarize_expenses(args):
    category = args.kategoria
    month = args.miesiac
    year = args.rok

    all_rows = get_all_expenses_main()
    if not all_rows:
        print("Nie można pokazać podsumowania, ponieważ nie dodano jeszcze żadnych wydatków")
        return
    date_from = args.data_od
    date_to = args.data_do
    data = filter_by_date(date_from, date_to, all_rows, args)
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    data = filter_by_amount(amount_from, amount_to, data)

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
            statistics_health = refine_statistics(calculate_expense_stats(data, "Zdrowie"), "Zdrowie")
            statistics_other = refine_statistics(calculate_expense_stats(data, "Inne"), "Inne")
            category_statistics = [
                statistics_food,
                statistics_shopping,
                statistics_transport,
                statistics_entertainment,
                statistics_health,
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
    create_backup(RECURRING_PATH)
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = f"{float(args.kwota):.2f}"
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
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    data = filter_by_amount(amount_from, amount_to, all_rows)

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
    create_backup(RECURRING_PATH)
    expense_id = args.id
    all_rows = load_recurring_expenses()
    all_rows = [row for row in all_rows if int(row[0]) != expense_id]
    write_all_recurring_expenses(all_rows)
    print(f"Usunięto wydatek (ID: {expense_id})")

def edit_recurring_expense(args):
    create_backup(RECURRING_PATH)
    expense_id = args.id
    date = args.data
    description = args.opis
    amount = f"{float(args.kwota):.2f}" if args.kwota is not None else None
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
    create_backup(CSV_PATH)
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
    create_backup(BUDGET_PATH)
    all_budgets = load_budgets()
    amount = f"{float(args.kwota):.2f}"
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
    provided_date_index = next((i for i, row in enumerate(all_budgets) if str(row[1]).zfill(4) == year and str(row[2]).zfill(2) == month), None)
    if provided_date_index is not None:
        all_budgets[provided_date_index][3] = amount
        all_budgets[provided_date_index][4] = status
    else:
        all_budgets.append([budget_id, year, month, amount, status])
    write_all_budgets(all_budgets)


def set_budget_off(args):
    create_backup(BUDGET_PATH)
    all_budgets = load_budgets()
    amount = ""
    id_list = [int(row[0]) for row in all_budgets if row[0] != 'ID']
    budget_id = max(id_list, default=0) + 1
    one_off = args.tylko_ten
    if one_off:
        status = "CURRENT"
    else:
        status = "OFF"
    if args.od:
        year, month = normalize_year_month(args.od)
    else:
        today = datetime.date.today()
        year = f"{today.year:04d}"
        month = f"{today.month:02d}"
    provided_date_index = next((i for i, row in enumerate(all_budgets) if str(row[1]).zfill(4) == year and str(row[2]).zfill(2) == month), None)
    if provided_date_index is not None:
        all_budgets[provided_date_index][3] = amount
        all_budgets[provided_date_index][4] = status
    else:
        all_budgets.append([budget_id, year, month, amount, status])
    write_all_budgets(all_budgets)


def remove_budget(args):
    create_backup(BUDGET_PATH)
    budget_id = args.id
    all_budgets = load_budgets()
    all_budgets = [row for row in all_budgets if int(row[0]) != budget_id]
    write_all_budgets(all_budgets)
    print(f"Usunięto budżet o ID: {budget_id}")

def current_budget(args):
    all_budgets = load_budgets()
    if not all_budgets:
        print("Aktualnie nie obowiązuje żaden budżet")
        return
    else:
        today = datetime.date.today()
        current_year, current_month = f"{today.year:04d}", f"{today.month:02d}"
        current_budget = next((row for row in reversed(all_budgets) if (str(row[1]).zfill(4), str(row[2]).zfill(2)) == (current_year, current_month) and row[4] == "CURRENT"), None)
        if current_budget:
            if current_budget[3] == "":
                print("W tym miesiącu budżet jest wyłączony (tylko ten miesiąc)")
            else:
                print(f"Aktualny budżet wynosi {float(current_budget[3]):.2f} zł na miesiąc (tylko ten miesiąc)")
        else:
            current_budget = next((row for row in reversed(all_budgets) if (str(row[1]).zfill(4), str(row[2]).zfill(2)) <= (current_year, current_month) and row[4] != "CURRENT"), None)
            if current_budget:
                if current_budget[3] == "":
                    print(f"Aktualnie nie obowiązuje żaden budżet (wyłączony od {current_budget[1]}-{current_budget[2]})")
                else:
                    print(f"Aktualny budżet wynosi {float(current_budget[3]):.2f} zł na miesiąc i obowiązuje od {current_budget[1]}-{current_budget[2]}")
            else:
                print("Aktualnie nie obowiązuje żaden budżet")

def list_budgets(args):
    all_budgets = load_budgets()
    status = args.status
    if not all_budgets:
        print("Brak budżetów do wyświetlenia")
        return
    data = filter_by_date_budgets(args, all_budgets)
    if status is not None:
        data = [row for row in data if row[4] == status]
    data = filter_by_amount_budgets(args, data)
    data = sort_budgets(data, args.sortuj_po, args.malejaco)
    if data:
        print(tabulate.tabulate(data, headers=['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status'], tablefmt="github", numalign="center"))
    else:
        print("Brak budżetów do wyświetlenia")

def raport_budget(args):
    all_budgets = load_budgets()
    date = args.data
    year, month = normalize_year_month(date)
    if all_budgets:
       budget_for_raport =  next((row for row in reversed(all_budgets) if (str(row[1]).zfill(4),str(row[2]).zfill(2)) <= (year,month)), None)
       if budget_for_raport is None:
           print("Nie można przeprowadzić raportu, nie ustawiono żadnego budżetu dla podanego miesiąca")
       else:
           if budget_for_raport[4]=="OFF" or (budget_for_raport[3]=="" and budget_for_raport[4]=="CURRENT"):
               print(f"W miesiącu {date}, budżet był wyłączony")
           else:
               sum_of_expenses = sum_expenses_in_month(date)
               if sum_of_expenses>float(budget_for_raport[3]):
                   print(f"W miesiącu {date}, budżet wynosił {budget_for_raport[3]}zł i został przekroczony o {sum_of_expenses-float(budget_for_raport[3])}zł.")
               else:
                   print(f"W miesiącu {date}, budżet wynosił {budget_for_raport[3]}zł i nie został on przekroczony. Można jeszcze wydać {float(budget_for_raport[3])-sum_of_expenses}zł.")
    else:
        print("Nie dodano jeszcze żadnego budżetu")

def export_expense(args):
    all_rows = get_all_expenses_main()
    category = args.kategoria
    headers = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria']
    if not all_rows:
        print("Nie można eksportować wydatków do pliku, ponieważ nie dodano jeszcze żadnych wydatków")
        return
    date_from = args.data_od
    date_to = args.data_do
    data = filter_by_date(date_from, date_to, all_rows, args)
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    data = filter_by_amount(amount_from, amount_to, data)
    if category is not None:
        data = [row for row in data if row[4] == category]
    file_type = args.format
    file_path = resolve_export_path(args.plik, file_type)
    if data:
        create_emergency_backup(file_path)
        if file_type == 'csv':
            data.insert(0, headers)
            export_to_csv(data, file_path)
            print(f"Wyeksportowano {len(data)-1} wydatków do {file_path}")
        elif file_type == 'json':
            data_dicts = [dict(zip(headers, row)) for row in data]
            metadata = create_expenses_metadata(args, data_dicts, 'wydatki.csv')
            export_to_json(data_dicts, file_path, metadata)
            print(f"Wyeksportowano {len(data_dicts)} wydatków do {file_path}")
        elif file_type == 'xlsx':
            metadata = create_expenses_metadata(args, data, 'wydatki.csv')
            export_to_excel(headers, data, file_path, metadata, "Wydatki")
            print(f"Wyeksportowano {len(data)} wydatków do {file_path}")
    else:
        print("Brak wydatków do wyeksportowania")

def export_recurring_expense(args):
    all_rows = load_recurring_expenses()
    category = args.kategoria
    frequency = args.czestotliwosc
    headers = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria', 'Częstotliwość']
    if not all_rows:
        print("Nie można eksportować wydatków cyklicznych do pliku, ponieważ nie dodano jeszcze żadnych wydatków")
        return
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    data = filter_by_amount(amount_from, amount_to, all_rows)
    if category is not None:
        data = [row for row in data if row[4] == category]
    if frequency is not None:
        data = [row for row in data if row[5] == frequency]
    file_type = args.format
    file_path = resolve_export_path(args.plik, file_type)
    if data:
        create_emergency_backup(file_path)
        if file_type == 'csv':
            data.insert(0, headers)
            export_to_csv(data, file_path)
            print(f"Wyeksportowano {len(data)-1} wydatków cyklicznych do {file_path}")
        elif file_type == 'json':
            data_dicts = [dict(zip(headers, row)) for row in data]
            metadata = create_expenses_metadata(args, data_dicts, 'recurring.csv')
            export_to_json(data_dicts, file_path, metadata)
            print(f"Wyeksportowano {len(data_dicts)} wydatków cyklicznych do {file_path}")
        elif file_type == 'xlsx':
            metadata = create_expenses_metadata(args, data, 'recurring.csv')
            export_to_excel(headers, data, file_path, metadata, "Wydatki cykliczne")
            print(f"Wyeksportowano {len(data)} wydatków cyklicznych do {file_path}")
    else:
        print("Brak wydatków cyklicznych do wyeksportowania")

def export_budget(args):
    all_rows = load_budgets()
    status = args.status
    file_type = args.format
    file_path = resolve_export_path(args.plik, file_type)
    if not all_rows:
        print("Nie można eksportować budżetów do pliku, ponieważ nie dodano jeszcze żadnych budżetów")
        return
    if args.tryb == 'ustawienia':
        data = filter_by_date_budgets(args, all_rows)
        data = filter_by_amount_budgets(args, data)
        if status is not None:
            data = [row for row in data if row[4] == status]
        headers = ['ID', 'Rok', 'Miesiąc', 'Kwota', 'Status']
    elif args.tryb == 'obowiazujace':
        data = expand_budgets_to_months(args, all_rows)
        if status is not None:
            data = [row for row in data if row[2] == status]
        if args.kwota_od or args.kwota_do:
            filtered = []
            for row in data:
                if row[1] == 'BRAK':
                    continue
                amount = float(row[1])
                if args.kwota_od and amount < args.kwota_od:
                    continue
                if args.kwota_do and amount > args.kwota_do:
                    continue
                filtered.append(row)
            data = filtered
        headers = ['Miesiąc', 'Kwota', 'Status', 'Źródło ID']
    if data:
        create_emergency_backup(file_path)
        if file_type == 'csv':
            data.insert(0, headers)
            export_to_csv(data, file_path)
            print(f"Wyeksportowano {len(data)-1} budżetów do {file_path}")
        elif file_type == 'json':
            data_dicts = [dict(zip(headers, row)) for row in data]
            metadata = create_expenses_metadata(args, data_dicts, 'budget.csv')
            export_to_json(data_dicts, file_path, metadata)
            print(f"Wyeksportowano {len(data_dicts)} budżetów do {file_path}")
        elif file_type == 'xlsx':
            metadata = create_expenses_metadata(args, data, 'budget.csv')
            export_to_excel(headers, data, file_path, metadata, "Budżety")
            print(f"Wyeksportowano {len(data)} budżetów do {file_path}")
    else:
        print("Brak budżetów do wyeksportowania")

def full_monthly_raport(args):
    year_month = args.rok+"-"+args.miesiac
    year, month = normalize_year_month(year_month)
    date_from = f"{year}-{month}-01"
    last_day = monthrange(int(year), int(month))[1]
    date_to = f"{year}-{month}-{last_day:02d}"
    print(f"\n{'='*50}")
    print(f"RAPORT MIESIĘCZNY: {MONTH_NAMES[int(month)]} {year}")
    print(f"{'='*50}")
    print(f"Okres: {date_from} do {date_to}\n")

    print_budget_section(year, month)
    print_expenses_section(date_from, date_to)
    print_recurring_section(year, month)
    print_top_expenses(date_from, date_to, n=5)


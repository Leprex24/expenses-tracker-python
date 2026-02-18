from calendar import monthrange
from datetime import timedelta, datetime, date
import tabulate

from tracker.file_ops import get_all_expenses_main, load_recurring_expenses, load_budgets
from dateutil.relativedelta import relativedelta


def id_exists(expense_id, rows=None):
    if rows is None:
        rows = get_all_expenses_main()
    id_list = [int(row[0]) for row in rows]
    return expense_id in id_list

def id_exists_recurring(expense_id, rows=None):
    if rows is None:
        rows = load_recurring_expenses()
    id_list = [int(row[0]) for row in rows]
    return expense_id in id_list

def filter_by_date(date_from, date_to, all_rows, args):
    if date_from is None and date_to is None:
        data = all_rows
    elif date_from is None and date_to is not None:
        data = [row for row in all_rows if row[1] <= date_to]
    elif date_from is not None and date_to is None:
        data = [row for row in all_rows if row[1] >= date_from]
    else:
        data = [row for row in all_rows if date_from <= row[1] <= date_to]
    if args:
        if args.mode == "wypisz":
            d = args.data
            if d is not None:
                data = [row for row in all_rows if row[1] == d]
    return data

def filter_by_amount(amount_min, amount_max, all_rows):
    if amount_min is None and amount_max is None:
        data = all_rows
    elif amount_min is not None and amount_max is None:
        data = [row for row in all_rows if float(row[3]) >= amount_min]
    elif amount_min is None and amount_max is not None:
        data = [row for row in all_rows if float(row[3]) <= amount_max]
    else:
        data = [row for row in all_rows if amount_min <= float(row[3]) <= amount_max]
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

def parse_date(d):
    return date.fromisoformat(d)

def date_to_string(d):
    return d.isoformat()

def find_last_due_date(recurring_expense, all_expenses):
    for expense in reversed(all_expenses):
        if expense[2] == recurring_expense[2] and expense[3] == recurring_expense[3] and expense[4] == recurring_expense[4]:
            return parse_date(expense[1])
    return parse_date(recurring_expense[1])

def is_end_of_month(d):
    return d.day == monthrange(d.year, d.month)[1]

def add_one_month(original_date):
    if original_date.month == 12:
        year, month = original_date.year + 1, 1
    else:
        year, month = original_date.year, original_date.month + 1

    last_day_next = monthrange(year, month)[1]

    if is_end_of_month(original_date):
        day = last_day_next
    else:
        day = min(original_date.day, last_day_next)

    return date(year, month, day)

def add_one_year(original_date):
    new_year = original_date.year + 1
    try:
        return original_date.replace(year=new_year)
    except ValueError:
        last_day_same_month = monthrange(new_year, original_date.month)[1]
        return original_date.replace(year=new_year, day=last_day_same_month)

def get_due_dates(start_date, frequency, until_date):
    if start_date > until_date:
        return []
    due_dates = []
    current = start_date
    if frequency == "Codzienne":
        while current <= until_date:
            due_dates.append(current)
            current += timedelta(days=1)
    elif frequency == "Tygodniowe":
        while current <= until_date:
            due_dates.append(current)
            current += timedelta(days=7)
    elif frequency == "Dwutygodniowe":
        while current <= until_date:
            due_dates.append(current)
            current += timedelta(days=14)
    elif frequency == "Miesięczne":
        while current <= until_date:
            due_dates.append(current)
            current = add_one_month(current)
    elif frequency == "Roczne":
        while current <= until_date:
            due_dates.append(current)
            current = add_one_year(current)
    return due_dates

def already_exists(rec, date_str, all_expenses):
    for expense in reversed(all_expenses):
        if expense[1] == date_str and expense[2] == rec[2] and expense[3] == rec[3] and expense[4] == rec[4]:
            return True
    return False

def normalize_year_month(d):
    dt = datetime.strptime(d, "%Y-%m")
    return f"{dt.year:04d}", f"{dt.month:02d}"

def filter_by_date_budgets(args, all_rows):
    date_from = args.data_od
    date_to = args.data_do
    if date_from is None and date_to is None:
        data = all_rows
    elif date_from is None and date_to is not None:
        year, month = normalize_year_month(date_to)
        data = [row for row in all_rows if (str(row[1]).zfill(4), str(row[2]).zfill(2)) <= (year, month)]
    elif date_from is not None and date_to is None:
        year, month = normalize_year_month(date_from)
        data = [row for row in all_rows if (str(row[1]).zfill(4), str(row[2]).zfill(2)) >= (year, month)]
    else:
        year_from, month_from = normalize_year_month(date_from)
        year_to, month_to = normalize_year_month(date_to)
        data = [row for row in all_rows if (year_from,month_from) <= (str(row[1]).zfill(4), str(row[2]).zfill(2)) <= (year_to, month_to)]

    return data

def filter_by_amount_budgets(args, all_rows):
    amount_from = args.kwota_od
    amount_to = args.kwota_do
    if amount_from is None and amount_to is None:
        data = all_rows
    else:
        data = [row for row in all_rows if row[3] != ""]
        if amount_from is None and amount_to is not None:
            data = [row for row in data if float(row[3]) <= amount_to]
        elif amount_from is not None and amount_to is None:
            data = [row for row in data if float(row[3]) >= amount_from]
        else:
            data = [row for row in data if amount_from <= float(row[3]) <= amount_to]
    return data

def sort_budgets(data, sort_by, reverse):
    key_map = {
        'ID': lambda x: int(x[0]),
        'Data': lambda x: (str(x[1]).zfill(4), str(x[2]).zfill(2)),
        'Kwota': lambda x: float(x[3].strip()) if str(x[3]).strip() != "" else 0.0,
        'Status': lambda x: x[4]
    }
    data.sort(key=key_map[sort_by], reverse=reverse)
    return data

def sum_expenses_in_month(month):
    all_expenses = get_all_expenses_main()
    data = [row for row in all_expenses if row[1].startswith(month)]
    sum_of_expenses = 0.0
    for expense in data:
        sum_of_expenses += float(expense[3])
    return sum_of_expenses

def id_exists_budgets(expense_id, rows=None):
    if rows is None:
        rows = load_budgets()
    id_list = [int(row[0]) for row in rows]
    return expense_id in id_list

def create_expenses_metadata(args, data, source):
    metadata = {
        'exported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source': source,
        'filters': {},
        'count': len(data),
    }
    possible_filters = [
        'kategoria', 'data_od', 'data_do', 'kwota_od', 'kwota_do', 'status', 'czestotliwosc',
    ]
    for filter in possible_filters:
        if hasattr(args, filter):
            value = getattr(args, filter)
            if value is not None:
                metadata['filters'][filter] = value
    return metadata

def expand_budgets_to_months(args, all_budgets):
    if args.data_od:
        start_year, start_month = normalize_year_month(args.data_od)
    else:
        start_year, start_month = str(all_budgets[0][1]).zfill(4), str(all_budgets[0][2]).zfill(2)
    if args.data_do:
        end_year, end_month = normalize_year_month(args.data_do)
    else:
        end_year, end_month = str(all_budgets[-1][1]).zfill(4), str(all_budgets[-1][2]).zfill(2)
    result = []
    current = date(int(start_year), int(start_month), 1)
    end = date(int(end_year), int(end_month), 1)
    while current <= end:
        year_str = f"{current.year:04d}"
        month_str = f"{current.month:02d}"
        current_budget = next((budget for budget in all_budgets if budget[4] == 'CURRENT' and (str(budget[1]).zfill(4), str(budget[2]).zfill(2)) == (year_str, month_str)), None)
        if current_budget:
            amount = current_budget[3] if current_budget[3] else 'BRAK'
            status = 'CURRENT'
            source_id = current_budget[0]
        else:
            active = next((budget for budget in reversed(all_budgets) if budget[4] != 'CURRENT' and (str(budget[1]).zfill(4), str(budget[2]).zfill(2)) <= (year_str, month_str)), None)
            if active:
                if active[4] == "OFF":
                    amount = 'BRAK'
                    status = 'OFF'
                else:
                    amount = active[3]
                    status = 'ON'
                source_id = active[0]
            else:
                amount = 'BRAK'
                status = 'Brak budżetu'
                source_id = '-'
        result.append([
            f"{year_str}-{month_str}",
            amount,
            status,
            f"Budżet #{source_id}"
        ])
        current = current.replace(day=1) + relativedelta(months=1)
    return result

def print_budget_section(year, month):
    all_budgets = load_budgets()
    print("\n --- BUDŻET --- ")
    if all_budgets:
       budget_for_raport =  next((row for row in reversed(all_budgets) if (str(row[1]).zfill(4),str(row[2]).zfill(2)) <= (year,month)), None)
       if budget_for_raport is None:
           print("Nie można przeprowadzić raportu, nie ustawiono żadnego budżetu dla podanego miesiąca")
       else:
           if budget_for_raport[4]=="OFF" or (budget_for_raport[3]=="" and budget_for_raport[4]=="CURRENT"):
               amount = None
           else:
               amount = float(budget_for_raport[3])
           print(f"Ustalony budżet: {amount if amount is not None else "Nie przydzielono budżetu"}")
           sum_of_expenses = sum_expenses_in_month(f'{year}-{month}')
           print(f"Wydano: {sum_of_expenses}")
           if amount is not None:
               print(f"Pozostało: {amount - sum_of_expenses}")
               print(f"Wykorzystano: {round(sum_of_expenses/amount*100,2)}%")
    else:
        print("Nie można przeprowadzić raportu, nie ustawiono żadnego budżetu dla podanego miesiąca")

def print_expenses_section(date_from, date_to):
    all_expenses = get_all_expenses_main()
    print("\n --- STATYSTYKI OGÓLNE --- ")
    filtered_expenses = filter_by_date(date_from, date_to, all_expenses, args=None)
    if filtered_expenses:
        stats = calculate_expense_stats(filtered_expenses)
        print(f"Liczba wydatków: {stats[0]}")
        print(f"Suma wydatków: {stats[1]} zł")
        print(f"Średni wydatek: {stats[2]} zł")
        print(f"Najwyższy wydatek: {stats[3]} zł (ID: {next(row[0] for row in filtered_expenses if float(row[3]) == stats[3])}, Data: {next(row[1] for row in filtered_expenses if float(row[3]) == stats[3])})")
        print(f"Najniższy wydatek: {stats[4]} zł (ID: {next(row[0] for row in filtered_expenses if float(row[3]) == stats[4])}, Data: {next(row[1] for row in filtered_expenses if float(row[3]) == stats[4])})")

        print_category_section(filtered_expenses)
    else:
        print("W podanym miesiącu nie zarejestrowano żadnych wydatków.")

def print_category_section(fitlered_expenses):
    print("\n --- STATYSTYKI KATEGORII --- ")
    categories = set(row[4] for row in fitlered_expenses)
    print(f"Kategorie występujące w tym miesiącu: {', '.join(categories)}")
    category_stats = []
    for category in categories:
        number = 0
        sum = 0
        for row in fitlered_expenses:
            if row[4] == category:
                number += 1
                sum += float(row[3])
        share = round(sum/float(len(fitlered_expenses)), 2)
        share_str = f"{share}%" if share >= 0.01 else "<1%"
        category_stats.append([category, number, sum, share_str])
    print(tabulate.tabulate(category_stats, headers=["Kategoria", "Liczba wydatków", "Suma wydatków", "Udział w wydatkach"], tablefmt="github", numalign="center", stralign="center"))

def get_reccuring_in_month(year, month, all_expenses=get_all_expenses_main(), all_recurring=load_recurring_expenses()):
    month_prefix = f"{year}-{month}"
    recurring_in_month = []
    for expense in all_expenses:
        if not expense[1].startswith(month_prefix):
            continue
        for rec in all_recurring:
            if expense[2] == rec[2] and expense[3] == rec[3] and expense[4] == rec[4]:
                recurring_in_month.append([rec[2], rec[3], expense[1]])
                break
    return recurring_in_month

def print_recurring_section(year, month):
    print("\n --- WYDATKI CYKLICZNE --- ")
    recurring_in_month = get_reccuring_in_month(year, month, get_all_expenses_main(), load_recurring_expenses())
    if recurring_in_month:
        print(f"Dodano {len(recurring_in_month)} wydatki cykliczne o łącznej wartości {sum(float(rec[1]) for rec in recurring_in_month)} zł")
        for rec in recurring_in_month:
            print(f" - {rec[0]}: {rec[1]} ({rec[2]})")
    else:
        print("W podanym miesiącu nie zarejestrowano żadnych wydatków cyklicznych.")

def print_top_expenses(date_from, date_to, n):
    all_expenses = get_all_expenses_main()
    filtered_expenses = filter_by_date(date_from, date_to, all_expenses, args=None)
    if filtered_expenses:
        print("\n --- TOP 5 WYDATKÓW --- ")
        top_expenses = sorted(filtered_expenses, key=lambda x: float(x[3]), reverse=True)[:n]
        i = 1
        for expense in top_expenses:
            print(f" {i}. {expense[3]} zł - {expense[2]} ({expense[1]})")
from calendar import monthrange
from datetime import timedelta, datetime, date

from tracker.file_ops import get_all_expenses_main, load_recurring_expenses, load_budgets


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
        d = args.data
        if d is not None:
            data = [row for row in all_rows if row[1] == d]
    return data

def filter_by_amount(args, all_rows):
    amount_min = args.kwota_od
    amount_max = args.kwota_do

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
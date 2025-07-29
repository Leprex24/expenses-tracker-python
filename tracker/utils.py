from tracker.file_ops import get_all_expenses


def id_exists(expense_id, rows=None):
    if rows is None:
        rows = get_all_expenses()
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
import datetime

from tracker.utils import id_exists, id_exists_recurring


def validate_date(date):
    if date is None:
        return True
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_year(year):
    if year is None:
        return True
    try:
        datetime.datetime.strptime(year, "%Y")
        return True
    except ValueError:
        return False

def validate_month(month):
    if month is None:
        return True
    try:
        datetime.datetime.strptime(month, "%m")
        return True
    except ValueError:
        return False

def validate_add(args):
    if not validate_date(args.data):
        return False, "Podano nieprawidłową datę"
    if id_exists(args.id):
        return False, "Podano już istniejące ID"
    return True, None

def validate_list(args):
    if args.data and (args.data_od or args.data_do):
        return False, "--data nie może być używana z --data-od lub --data-do"
    for data in [args.data_od, args.data_do, args.data]:
        if data and not validate_date(data):
            return False, "Podano nieprawidłową datę"
    if args.data_do and args.data_od and args.data_do < args.data_od:
        return False, "--data-do nie może być wcześniejsza niż --data-od"
    if args.kwota_do and args.kwota_od and args.kwota_do < args.kwota_od:
        return False, "--kwota-do nie może być mniejsza od --kwota-od"
    return True, None

def validate_delete(args):
    if not id_exists(args.id):
        return False, f"Wydatek o ID: {args.id} nie istnieje"
    return True, None

def validate_edit(args):
    if not validate_date(args.data):
        return False, "Podano nieprawidłową datę"
    if not id_exists(args.id):
        return False, f"Wydatek o ID: {args.id} nie istnieje"
    return True, None

def validate_summary(args):
    if args.miesiac and not args.rok:
        return False, "Aby wyświetlić podsumowanie konkretnego miesiąca musisz podać --rok"
    if args.data_do and args.data_od and args.data_do < args.data_od:
        return False, "--data-do nie może być wcześniejsza niż --data-od"
    if (args.miesiac or args.rok) and (args.data_do or args.data_od):
        return False, "--miesiac i --rok nie mogą być używane jednocześnie z --data-od i --data-do"
    for date in [args.data_do, args.data_od]:
        if date and not validate_date(date):
            return False, "Podano nieprawidłową datę"
    if args.rok and not validate_year(args.rok):
        return False, "Podano nieprawidłowy rok"
    if args.miesiac and not validate_month(args.miesiac):
        return False, "Podano nieprawidłowy miesiąc"
    if args.kwota_do and args.kwota_od and args.kwota_do < args.kwota_od:
        return False, "--kwota-do nie może być mniejsza od --kwota-od"
    return True, None

def validate_recurring_edit(args):
    if not validate_date(args.data):
        return False, "Podano nieprawidłową datę"
    if not id_exists_recurring(args.id):
        return False, f"Wydatek cykliczny o id {args.id} nie istnieje"
    return True, None

def validate_recurring_add(args):
    if not validate_date(args.data):
        return False, "Podano nieprawidłową datę"
    if id_exists_recurring(args.id):
        return False, "Podano już istniejące ID"
    return True, None

def validate_recurring_delete(args):
    if not id_exists_recurring(args.id):
        return False, f"Wydatek cykliczny o ID: {args.id} nie istnieje"
    return True, None

def validate_recurring_list(args):
    if args.kwota_do and args.kwota_od and args.kwota_do < args.kwota_od:
        return False, "--kwota-do nie może być mniejsza od --kwota-od"
    return True, None
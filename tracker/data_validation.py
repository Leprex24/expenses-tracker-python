import os
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
LOG_PATH = os.path.join(LOGS_DIR, 'validation_log.txt')
VALID_CATEGORIES = ['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Zdrowie', 'Inne']
VALID_FREQUENCIES = ['Codzienne', 'Tygodniowe', 'Dwutygodniowe', 'Miesięczne', 'Roczne']
VALID_STATUS = ['ON', 'OFF', 'CURRENT']

def add_validation_logs(errors, file_name):
    os.makedirs(LOGS_DIR, exist_ok=True)
    with open(LOG_PATH, 'a', encoding='utf-8') as logfile:
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        logfile.write(f"{timestamp} - {file_name}\n")
        for error in errors:
            logfile.write("   - "+error + "\n")
        logfile.write("\n")

def try_fix_date(date_str):
    if not date_str or not date_str.strip():
        return None, False
    date_str = date_str.strip()
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str, False
    except ValueError:
        pass
    formats_to_try = [
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%d.%m.%Y"
    ]
    for fmt in formats_to_try:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.date().isoformat(), True
        except ValueError:
            continue
    normalized = date_str.replace('/', '-').replace('.', '-')
    parts = normalized.split('-')
    if len(parts) == 3:
        try:
            if len(parts[0]) == 4 and parts[0].isdigit():
                year, month, day = parts
                if month.isdigit() and day.isdigit():
                    fixed = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    datetime.strptime(fixed, "%Y-%m-%d")
                    return fixed, True
            elif len(parts[2]) == 4 and parts[2].isdigit():
                day, month, year = parts
                if month.isdigit() and day.isdigit():
                    fixed = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    datetime.strptime(fixed, "%Y-%m-%d")
                    return fixed, True
        except ValueError:
            pass
    return None, False

def validate_and_fix_expenses(all_rows):
    errors = []
    fixed_rows = []
    seen_ids = set()
    i = 1
    for row in all_rows:
        try:
            exp_id = int(row[0])
            if exp_id <= 0:
                errors.append(f"Usunięto rekord #{i}: ID ujemne lub zero ({exp_id})")
                i += 1
                continue
            if exp_id in seen_ids:
                errors.append(f"Usunięto rekord #{i}: Duplikat ID ({exp_id})")
                i += 1
                continue
            seen_ids.add(exp_id)
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowe ID ({row[0]})")
            i += 1
            continue
        original_date = row[1]
        fixed_date, was_fixed = try_fix_date(row[1])
        if fixed_date:
            row[1] = fixed_date
            if was_fixed:
                errors.append(f"Poprawiono datę w rekordzie #{i}: {original_date} -> {fixed_date}")
        else:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa data ({row[1]})")
            i += 1
            continue
        if not row[2] or row[2].strip() == "":
            row[2] = "Brak opisu"
            errors.append(f"Dodano opis w rekordzie #{i}: 'Brak opisu'")
        try:
            amount = float(row[3])
            if amount <= 0:
                errors.append(f"Usunięto rekord #{i}: Kwota nie może być ujemna lub zero ({row[3]})")
                i += 1
                continue
            original_amount = row[3]
            row[3] = f"{round(amount, 2):.2f}"
            if original_amount != row[3]:
                errors.append(f"Poprawiono kwotę w rekordzie #{i}: {original_amount} -> {row[3]}")
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa kwota ({row[3]})")
            i += 1
            continue
        if row[4] not in VALID_CATEGORIES:
            original_category = row[4] if row[4] else "(pusta)"
            row[4] = "Inne"
            errors.append(f"Poprawiono kategorię w rekordzie #{i}: {original_category} -> 'Inne'")
        if len(row) != 5:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa liczba kolumn ({len(row)})")
            i += 1
            continue
        fixed_rows.append(row)
        i += 1
    return fixed_rows, errors

def validate_and_fix_recurring(all_rows):
    errors = []
    fixed_rows = []
    seen_ids = set()
    i = 1
    for row in all_rows:
        try:
            exp_id = int(row[0])
            if exp_id <= 0:
                errors.append(f"Usunięto rekord #{i}: ID ujemne lub zero ({exp_id})")
                i += 1
                continue
            if exp_id in seen_ids:
                errors.append(f"Usunięto rekord #{i}: Duplikat ID ({exp_id})")
                i += 1
                continue
            seen_ids.add(exp_id)
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowe ID ({row[0]})")
            i += 1
            continue
        original_date = row[1]
        fixed_date, was_fixed = try_fix_date(row[1])
        if fixed_date:
            row[1] = fixed_date
            if was_fixed:
                errors.append(f"Poprawiono datę w rekordzie #{i}: {original_date} -> {fixed_date}")
        else:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa data ({row[1]})")
            i += 1
            continue
        if not row[2] or row[2].strip() == "":
            row[2] = "Brak opisu"
            errors.append(f"Dodano opis w rekordzie #{i}: 'Brak opisu'")
        try:
            amount = float(row[3])
            if amount <= 0:
                errors.append(f"Usunięto rekord #{i}: Kwota nie może być ujemna lub zero ({row[3]})")
                i += 1
                continue
            original_amount = row[3]
            row[3] = f"{round(amount, 2):.2f}"
            if original_amount != row[3]:
                errors.append(f"Poprawiono kwotę w rekordzie #{i}: {original_amount} -> {row[3]}")
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa kwota ({row[3]})")
            i += 1
            continue
        if row[4] not in VALID_CATEGORIES:
            original_category = row[4] if row[4] else "(pusta)"
            row[4] = "Inne"
            errors.append(f"Poprawiono kategorię w rekordzie #{i}: {original_category} -> 'Inne'")
        if row[5] not in VALID_FREQUENCIES:
            original_frequency = row[5] if row[5] else "(pusta)"
            errors.append(f"Usunięto rekord #{i}: nieprawidłowa częstotliwość ({original_frequency})")
            i += 1
            continue
        if len(row) != 6:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa liczba kolumn ({len(row)})")
            i += 1
            continue
        fixed_rows.append(row)
        i += 1
    return fixed_rows, errors

def validate_and_fix_budgets(all_rows):
    errors = []
    fixed_rows = []
    seen_ids = set()
    i = 1
    for row in all_rows:
        try:
            budget_id = int(row[0])
            if budget_id <= 0:
                errors.append(f"Usunięto rekord #{i}: ID ujemne lub zero ({budget_id})")
                i += 1
                continue
            if budget_id in seen_ids:
                errors.append(f"Usunięto rekord #{i}: Duplikat ID ({budget_id})")
                i += 1
                continue
            seen_ids.add(budget_id)
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowe ID ({row[0]})")
            i += 1
            continue

        if not row[1] or row[1].strip() == "":
            errors.append(f"Usunięto rekord #{i}: Pusty rok")
            i += 1
            continue
        year_str = row[1].strip()
        try:
            year_int = int(year_str)
            if year_int < 1900 or year_int > 2100:
                errors.append(f"Usunięto rekord #{i}: Rok poza zakresem ({year_str})")
                i += 1
                continue
            row[1] = f"{year_int:04d}"
            if year_str != row[1]:
                errors.append(f"Poprawiono rok w rekordzie #{i}: {year_str} -> {row[1]}")
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowy rok ({year_str})")
            i += 1
            continue

        if not row[2] or row[2].strip() == "":
            errors.append(f"Usunięto rekord #{i}: Pusty miesiąc")
            i += 1
            continue
        month_str = row[2].strip()
        try:
            month_int = int(month_str)
            if month_int < 1 or month_int > 12:
                errors.append(f"Usunięto rekord #{i}: Nieprawidłowy miesiąc ({month_str})")
                i += 1
                continue
            original_month = month_str
            row[2] = f"{month_int:02d}"
            if original_month != row[2]:
                errors.append(f"Poprawiono miesiąc w rekordzie #{i}: {original_month} -> {row[2]}")
        except ValueError:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowy miesiąc ({row[2]})")
            i += 1
            continue

        amount_str = row[3].strip() if row[3] else ""
        amount_value = None
        if amount_str != "":
            try:
                amount_value = float(amount_str)
                if amount_value < 0:
                    errors.append(f"Usunięto rekord #{i}: Kwota ujemna ({amount_str})")
                    i += 1
                    continue
            except ValueError:
                errors.append(f"Usunięto rekord #{i}: Nieprawidłowa kwota ({amount_str})")
                i += 1
                continue

        original_status = row[4]
        if original_status not in VALID_STATUS:
            if amount_value is None or amount_value == 0:
                row[3] = ""
                row[4] = "OFF"
                errors.append(f"Poprawiono w rekordzie #{i}: {original_status} -> 'OFF' (pusta lub zerowa kwota)")
            else:
                row[3] = f"{round(amount_value, 2):.2f}"
                row[4] = "ON"
                errors.append(f"Poprawiono w rekordzie #{i}: {original_status} -> 'ON' (dodatnia kwota)")
        else:
            if amount_value is None or amount_value == 0:
                if original_status == "ON":
                    row[3] = ""
                    row[4] = "OFF"
                    errors.append(f"Poprawiono w rekordzie #{i}: brak kwoty przy statusie ON -> pusta kwota i status OFF")
                else:
                    row[3] = ""
                    if amount_str != "" and amount_str != row[3]:
                        errors.append(f"Poprawiono kwotę w rekordzie #{i}: {amount_str} -> pusta kwota")
            else:
                original_amount = row[3]
                row[3] = f"{round(amount_value, 2):.2f}"
                if original_amount != row[3]:
                    errors.append(f"Poprawiono kwotę w rekordzie #{i}: {original_amount} -> {row[3]}")
                if original_status == "OFF":
                    row[4] = "ON"
                    errors.append(f"Poprawiono status w rekordzie #{i}: dodatnia kwota przy statusie OFF -> status ON")
        if len(row) != 5:
            errors.append(f"Usunięto rekord #{i}: Nieprawidłowa liczba kolumn ({len(row)})")
            i += 1
            continue
        fixed_rows.append(row)
        i += 1
    return fixed_rows, errors


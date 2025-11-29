import argparse

from tracker.commands import add_expense, list_expenses, delete_expense, edit_expense, summarize_expenses, \
    add_recurring_expense, list_recurring_expenses, delete_recurring_expense, edit_recurring_expense, \
    sync_recurring_expenses, set_budget, remove_budget, list_budgets, set_budget_off, raport_budget, current_budget, \
    export_expense, export_recurring_expense, export_budget
from tracker.file_ops import file_verification_main, file_verification_recurring, file_verification_budget
from tracker.validators import validate_add, validate_delete, validate_edit, validate_list, validate_summary, \
    validate_recurring_edit, validate_recurring_add, validate_recurring_list, validate_recurring_delete, \
    validate_set_budget, validate_remove_budget, validate_list_budget, validate_turn_off_budget, validate_raport_budget, \
    validate_current_budget, validate_expenses_export, validate_recurring_export, validate_budget_export


def main():
    file_verification_main()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode', help='Dostepne tryby')

    add_parser = subparsers.add_parser('dodaj', help='Dodaj nowy wydatek')
    add_parser.add_argument('-o', '--opis', type=str, required=True ,help='Opis wydatku')
    add_parser.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    add_parser.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyślnie data dzisiejsza')
    add_parser.add_argument('--id', type=int, help='Niestandardowe ID')
    add_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Kategoria wydatku, domyślnie zakupy')

    list_parser = subparsers.add_parser('wypisz', help='Wypisz wszystkie wydatki')
    list_parser.add_argument('-k', '--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka'], help='Kategoria wydatków')
    list_parser.add_argument('--data-od', help='Data początkowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data-do', help='Data końcowa wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('--data', help='Konkretna data wyświetlanych wydatków (YYYY-MM-DD)')
    list_parser.add_argument('-s', '--sortuj-po', choices=['ID', 'Data', 'Kwota', 'Kategoria'], help='Sortowanie wydatków, domyślnie ID', default='ID')
    list_parser.add_argument('--malejaco', action='store_true', help='Sortuj malejąco, domyślnie rosnąco')
    list_parser.add_argument('--kwota-od', type=float ,help='Minimalna kwota wyświetlanych wydatków')
    list_parser.add_argument('--kwota-do', type=float ,help='Maksymalna kwota wyświetlanych wydatków')

    delete_parser = subparsers.add_parser('usun', help='Usuń istniejący wydatek')
    delete_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do usunięcia')

    edit_parser = subparsers.add_parser('edytuj', help='Edytuj wydatek')
    edit_parser.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do edycji')
    edit_parser.add_argument('-o', '--opis', type=str, help='Nowy opis wydatku')
    edit_parser.add_argument('-k', '--kwota', type=float, help='Nowa kwota wydatku')
    edit_parser.add_argument('-d', '--data', help='Nowa data wydatku (YYYY-MM-DD)')
    edit_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Nowa kategoria wydatku')

    summary_parser = subparsers.add_parser('podsumowanie', help='Podsumowanie wydatków')
    summary_parser.add_argument('-k' ,'--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka'], help='Kategoria wydatków do podsumowania')
    summary_parser.add_argument('-m', '--miesiac', type=str, help='Miesiac wydatków do podsumowania (MM)')
    summary_parser.add_argument('-r', '--rok', type=str, help='Rok wydatków do podsumowania (YYYY)')
    summary_parser.add_argument('--data-od', help='Data początkowa wydatków do podsumowania (YYYY-MM-DD)')
    summary_parser.add_argument('--data-do', help='Data końcowa wydatków do podsumowania (YYYY-MM-DD)')
    summary_parser.add_argument('--kwota-od', type=float ,help='Minimalna kwota wyświetlanych wydatków')
    summary_parser.add_argument('--kwota-do', type=float ,help='Maksymalna kwota wyświetlanych wydatków')

    recurring_parser = subparsers.add_parser('cykliczne', help="Zarządzaj wydatkami cyklicznymi")
    recurring_subparsers = recurring_parser.add_subparsers(dest="recurring_mode")

    recurring_add = recurring_subparsers.add_parser('dodaj', help='Dodaj wydatek cykliczny')
    recurring_add.add_argument('-o', '--opis', type=str, required=True, help='Opis wydatku')
    recurring_add.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    recurring_add.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyślnie data dzisiejsza')
    recurring_add.add_argument('--id', type=int, help='Niestandardowe ID')
    recurring_add.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Kategoria wydatku, domyślnie zakupy')
    recurring_add.add_argument('--czestotliwosc', choices=['Codzienne', 'Tygodniowe', 'Dwutygodniowe', 'Miesięczne', 'Roczne'], required=True, help='Częstotliwość wydatku')

    recurring_list = recurring_subparsers.add_parser('wypisz', help='Wypisz cykliczne wydatki')
    recurring_list.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka'], help='Kategoria wydatków')
    recurring_list.add_argument('--czestotliwosc', choices=['Codzienne', 'Tygodniowe', 'Dwutygodniowe', 'Miesięczne', 'Roczne'], help='Częstotliwość wydatków')
    recurring_list.add_argument('--sortuj-po', choices=['ID', 'Data', 'Kwota', 'Kategoria', 'Częstotliwość'], help='Sortowanie wydatków, domyślnie ID', default='ID')
    recurring_list.add_argument('--malejaco', action='store_true', help='Sortuj malejąco, domyślnie rosnąco')
    recurring_list.add_argument('--kwota-od', type=float ,help='Minimalna kwota wyświetlanych wydatków')
    recurring_list.add_argument('--kwota-do', type=float ,help='Maksymalna kwota wyświetlanych wydatków')

    recurring_remove = recurring_subparsers.add_parser('usun', help='Usuń wydatek cykliczny')
    recurring_remove.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do usunięcia')

    recurring_edit = recurring_subparsers.add_parser('edytuj', help="Edytuj wydatek cykliczny")
    recurring_edit.add_argument('-i', '--id', type=int, required=True, help='ID wydatku do edytuj')
    recurring_edit.add_argument('-o', '--opis', type=str, help='Nowy opis wydatku')
    recurring_edit.add_argument('-k', '--kwota', type=float, help='Nowa kwota wydatku')
    recurring_edit.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Nowa kategoria wydatku')
    recurring_edit.add_argument('--czestotliwosc', choices=['Codzienne', 'Tygodniowe', 'Dwutygodniowe', 'Miesięczne', 'Roczne'], help='Nowa częstotliwość wydatku')
    recurring_edit.add_argument('-d', '--data', help='Nowa data wydatku (YYYY-MM-DD)')

    budget_parser = subparsers.add_parser('budzet', help='Zarządzaj budżetem wydatków')
    budget_subparsers = budget_parser.add_subparsers(dest='budget_mode')

    budget_set = budget_subparsers.add_parser('ustaw', help='Ustaw budżet')
    budget_set.add_argument('-k', '--kwota', type=float, help='Kwota budżetu', required=True)
    budget_set.add_argument('--od', help='Od kiedy obowiązuje ustawiany budżet(YYYY-MM), domyślnie data aktualna')
    budget_set.add_argument('--tylko-ten', action="store_true", help='Ustawienie budżetu tylko dla tego miesiąca')

    budget_remove = budget_subparsers.add_parser('usun', help='Usuń zapis budżetu')
    budget_remove.add_argument('-i', '--id', type=int, required=True, help='ID budżetu do usunięcia')

    budget_list = budget_subparsers.add_parser('wypisz', help='Wypisz budżety zapisane w pliku CSV')
    budget_list.add_argument('--data-od', help='Filtr od jakiej daty wyświetlić budżety')
    budget_list.add_argument('--data-do', help='Filtr do jakiej daty wyświetlić budżety')
    budget_list.add_argument('--status', choices=['ON', 'OFF', 'CURRENT'], help='Filtr po statusie budżetu')
    budget_list.add_argument('--sortuj-po', choices=['ID', 'Data', 'Kwota', 'Status'], help='Sortowanie budżetów, domyślnie data', default='Data')
    budget_list.add_argument('--malejaco', action='store_true', help='Sortuj malejąco, domyślnie rosnąco')
    budget_list.add_argument('--kwota-od', type=float, help='Filtr początkowy kwoty budżetu')
    budget_list.add_argument('--kwota-do', type=float, help='Filtr końcowy kwoty budżetu')

    budget_off = budget_subparsers.add_parser('wylacz', help='Wyłącz budżet')
    budget_off.add_argument('--od', help='Od kiedy wyłączyć budżet(YYYY-MM), domyślnie data aktualna')
    budget_off.add_argument('--tylko-ten', action="store_true", help='Wyłączenie budżetu tylko dla tego miesiąca')

    budget_raport = budget_subparsers.add_parser('raport', help='Pokaż raport podanego miesiaca')
    budget_raport.add_argument('--data', required=True, help='Data budżetu do raportu (YYYY-MM)')

    budget_current = budget_subparsers.add_parser('aktualny', help='Pokaż aktualny budżet')

    export_parser = subparsers.add_parser('eksport', help="Eksportuj dane do pliku")
    export_subparsers = export_parser.add_subparsers(dest='export_mode')

    export_expenses = export_subparsers.add_parser('wydatki', help='Eksportuj wydatki do pliku')
    export_expenses.add_argument('--format', choices=['csv', 'json','xlsx'], help='Format pliku do eksportu', default="csv")
    export_expenses.add_argument('--plik', required=True, help='Nazwa pliku lub ścieżka do eksportu')
    export_expenses.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne'], help="Filtr kategori wydatków do eskportu")
    export_expenses.add_argument('--data-od', help="Filtr daty początkowej wydatków do eskportu")
    export_expenses.add_argument('--data-do', help="Filtr daty końcowej wydatków do eskportu")
    export_expenses.add_argument('--kwota-od', type=float,help="Filtr kwoty początkowej wydatków do eskportu")
    export_expenses.add_argument('--kwota-do', type=float, help="Filtr kwoty końcowej wydatków do eskportu")

    export_recurring = export_subparsers.add_parser('cykliczne', help='Eksportuj wydatki cykliczne do pliku')
    export_recurring.add_argument('--format', choices=['csv', 'json','xlsx'], help='Format pliku do eksportu', default="csv")
    export_recurring.add_argument('--plik', required=True, help='Nazwa pliku lub ścieżka do eksportu')
    export_recurring.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne'],help="Filtr kategori wydatków cyklicznych do eskportu")
    export_recurring.add_argument('--czestotliwosc', choices=['Codzienne', 'Tygodniowe', 'Dwutygodniowe', 'Miesięczne', 'Roczne'], help="Filtr częstotliwości wydatków cyklicznych do eskportu")
    export_recurring.add_argument('--kwota-od', type=float, help="Filtr kwoty początkowej wydatków cyklicznych do eskportu")
    export_recurring.add_argument('--kwota-do', type=float, help="Filtr kwoty końcowej wydatków cyklicznych do eskportu")

    export_budgets = export_subparsers.add_parser('budzet', help='Eksportuj budżety do pliku')
    export_budgets.add_argument('--format', choices=['csv', 'json','xlsx'], help='Format pliku do eksportu (domyślnie csv)', default="csv")
    export_budgets.add_argument('--plik', required=True, help='Nazwa pliku lub ścieżka do eksportu')
    export_budgets.add_argument('--tryb', choices=['ustawienia', 'obowiazujace'], default='ustawienia', help="Tryb eksportu: ustawienia (kiedy zostały ustawione) lub obowiazujace (rozwiniete na miesiace)")
    export_budgets.add_argument('--data-od', help="Filtr daty początkowej budżetów do eskportu")
    export_budgets.add_argument('--data-do', help="Filtr daty końcowej budżetów do eskportu")
    export_budgets.add_argument('--kwota-od', type=float, help="Filtr kwoty początkowej budżetów do eskportu")
    export_budgets.add_argument('--kwota-do', type=float, help="Filtr kwoty końcowej budżetów do eskportu")
    export_budgets.add_argument('--status', choices=['ON', 'OFF', 'CURRENT'], help='Filtr statusu budżetów do eskportu')

    args = parser.parse_args()

    if args.mode == 'cykliczne':
        file_verification_recurring()
        validators = {
            'dodaj': validate_recurring_add,
            'wypisz': validate_recurring_list,
            'usun': validate_recurring_delete,
            'edytuj': validate_recurring_edit,
        }
        handlers = {
            'dodaj': add_recurring_expense,
            'wypisz': list_recurring_expenses,
            'usun': delete_recurring_expense,
            'edytuj': edit_recurring_expense,
        }
        validator = validators.get(args.recurring_mode)
        handler = handlers.get(args.recurring_mode)
        if validator:
            valid, error_msg = validator(args)
            if not valid:
                parser.error(error_msg)
        if handler:
            handler(args)
        else:
            parser.print_help()
    elif args.mode == 'budzet':
        file_verification_budget()
        validators = {
            'ustaw': validate_set_budget,
            'usun': validate_remove_budget,
            'wypisz': validate_list_budget,
            'wylacz': validate_turn_off_budget,
            'raport': validate_raport_budget,
            'aktualny': validate_current_budget,
        }
        handlers = {
            'ustaw': set_budget,
            'usun': remove_budget,
            'wypisz': list_budgets,
            'wylacz': set_budget_off,
            'raport': raport_budget,
            'aktualny': current_budget,
        }
        validator = validators.get(args.budget_mode)
        handler = handlers.get(args.budget_mode)
        if validator:
            valid, error_msg = validator(args)
            if not valid:
                parser.error(error_msg)
        if handler:
            handler(args)
        else:
            parser.print_help()
    elif args.mode == 'eksport':
        validators = {
            'wydatki': validate_expenses_export,
            'cykliczne': validate_recurring_export,
            'budzet': validate_budget_export,
        }
        handlers = {
            'wydatki': export_expense,
            'cykliczne': export_recurring_expense,
            'budzet': export_budget,
        }
        validator = validators.get(args.export_mode)
        handler = handlers.get(args.export_mode)
        if validator:
            valid, error_msg = validator(args)
            if not valid:
                parser.error(error_msg)
        if handler:
            handler(args)
        else:
            parser.print_help()
    else:
        sync_recurring_expenses()
        validators = {
            'dodaj': validate_add,
            'wypisz': validate_list,
            'usun': validate_delete,
            'edytuj': validate_edit,
            'podsumowanie': validate_summary,
        }
        if args.mode in validators:
            valid, error_msg = validators[args.mode](args)
            if not valid:
                parser.error(error_msg)
            handler = {
                'dodaj': add_expense,
                'wypisz': list_expenses,
                'usun': delete_expense,
                'edytuj': edit_expense,
                'podsumowanie': summarize_expenses,
            }[args.mode]
            handler(args)
        else:
            parser.print_help()

if __name__ == '__main__':
    main()
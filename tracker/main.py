import argparse

from tracker.commands import add_expense, list_expenses, delete_expense, edit_expense, summarize_expenses
from tracker.file_ops import file_verification
from tracker.validators import validate_add, validate_delete, validate_edit, validate_list, validate_summary


def main():
    file_verification()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='mode', help='Dostepne tryby')

    add_parser = subparsers.add_parser('dodaj', help='Dodaj nowy wydatek')
    add_parser.add_argument('-o', '--opis', type=str, required=True ,help='Opis wydatku')
    add_parser.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    add_parser.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyślnie data dzisiejsza')
    add_parser.add_argument('--id', type=int, help='Niestandardowe ID')
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
    edit_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Nowa kategoria wydatku')

    summary_parser = subparsers.add_parser('podsumowanie', help='Podsumowanie wydatków')
    summary_parser.add_argument('-k' ,'--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka'], help='Kategoria wydatków do podsumowania')
    summary_parser.add_argument('-m', '--miesiac', type=str, help='Miesiac wydatków do podsumowania (MM)')
    summary_parser.add_argument('-r', '--rok', type=str, help='Rok wydatków do podsumowania (YYYY)')
    summary_parser.add_argument('--data-od', help='Data początkowa wydatków do podsumowania (YYYY-MM-DD)')
    summary_parser.add_argument('--data-do', help='Data końcowa wydatków do podsumowania (YYYY-MM-DD)')

    args = parser.parse_args()

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

    if args.mode == 'dodaj':
        add_expense(args)
    elif args.mode == 'wypisz':
        list_expenses(args)
    elif args.mode == 'usun':
        delete_expense(args)
    elif args.mode == 'edytuj':
        edit_expense(args)
    elif args.mode == 'podsumowanie':
        summarize_expenses(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
import argparse
import datetime
import csv
import tabulate
import os

def Sprawdzenie_pliku(nazwa_pliku='wydatki.csv'):
    if not os.path.exists(nazwa_pliku):
        with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
        print(f"Utworzono nowy plik: {nazwa_pliku}")
    else:
        with open(nazwa_pliku, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            oczekiwane_kolumny = ['ID', 'Data', 'Opis', 'Kwota', 'Kategoria']
            if header == oczekiwane_kolumny:
                print(f"Plik {nazwa_pliku} juz istnieje w poprawnym formacie")
            else:
                nadpis = int(input(f"Plik {nazwa_pliku} juz istnieje ale w innym formacie, czy chcesz go nadpisac? Podaj 1 dla tak lub 0 dla nie: "))
                while nadpis != 1 and nadpis != 0:
                    nadpis = int(input("Podana zla wartosc sprobuj jeszcze raz:"))
                if nadpis == 1:
                    with open(nazwa_pliku, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'])
                    print(f"Nadpisano plik: {nazwa_pliku}")

def dodaj_wydatek(args):
    ID = args.id
    data = args.data
    opis = args.opis
    kwota = args.kwota
    kategoria = args.kategoria

    if ID == None:
        with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            ID_lista = [int(wiersz[0]) for wiersz in reader if wiersz[0] != 'ID']
            ID = max(ID_lista, default=0)+1

    if data == None:
        data = datetime.datetime.now().strftime("%Y-%m-%d")

    if kategoria == None:
        kategoria = "Zakupy"

    with open('wydatki.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([ID, data, opis, kwota, kategoria])

    print(f"Dodano nowy wydatek (ID: {ID})")

def wypisz_wydatki(args):
    kategoria = args.kategoria
    suma = 0
    with open('wydatki.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        wszystkie_wiersze = list(reader)
        dane = []
        if not wszystkie_wiersze:
            print("Nie dodano jeszcze zadnych wydatkow")
            return

        if kategoria == None:
            dane = wszystkie_wiersze
        else:
            dane = [wiersz for wiersz in wszystkie_wiersze if wiersz[4] == kategoria]

        for wiersz in dane:
            suma += float(wiersz[3])

        if dane:
            print(tabulate.tabulate(dane, headers=['ID', 'Data', 'Opis', 'Kwota', 'Kategoria'], tablefmt="github"))
            print(f"Suma: {suma:.2f} zl")
        else:
            print("Brak wydatków do wyswietlenia")


def main():
    Sprawdzenie_pliku()
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tryb', help='Dostepne tryby')

    add_parser = subparsers.add_parser('dodaj', help='Dodaj nowy wydatek')
    add_parser.add_argument('-o', '--opis', type=str, required=True ,help='Opis wydatku')
    add_parser.add_argument('-k', '--kwota', type=float, required=True, help='Kwota wydatku')
    add_parser.add_argument('--data', help='Niestandardowa data (YYYY-MM-DD), domyslnie data dzisiejsza')
    add_parser.add_argument('--id', help='Niestandardowe ID')
    add_parser.add_argument('--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka', 'Inne' ], help='Kategoria wydatku, domyslnie zakupy')

    list_parser = subparsers.add_parser('wypisz', help='Wypisz wszystkie wydatki')
    list_parser.add_argument('-k', '--kategoria', choices=['Jedzenie', 'Zakupy', 'Transport', 'Rozrywka' ], help='Kategoria wydatku')

    args = parser.parse_args()

    if args.tryb == 'dodaj':
        dodaj_wydatek(args)

    if args.tryb == 'wypisz':
        wypisz_wydatki(args)

    if not args.tryb:
        parser.print_help()

if __name__ == '__main__':
    main()
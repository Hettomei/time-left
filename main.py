"""
Prend des input

ex:
debut : 8h32
fin   : 12h45
08h32 - 12h45  4:13:00   4:13:00

debut : 13h45
fin   : 18
08h32 - 12h45  4:13:00   4:13:00
13h45 - 18h00  4:15:00   8:28:00
"""
from datetime import datetime, timedelta
import sys


def to_datetime(_str):
    try:
        return datetime.strptime(_str, "%Hh%M")
    except ValueError:
        try:
            return datetime.strptime(_str, "%H:%M")
        except ValueError:
            return datetime.strptime(_str, "%H")


def add_date(date_list):
    debut = input("debut : ")
    d_debut = to_datetime(debut)

    fin = input("fin   : ")
    d_fin = to_datetime(fin)
    date_list.append([d_debut, d_fin])


def hour_sec(_datetime):
    return datetime.strftime(_datetime, "%Hh%M")


def show_diff(date_list):
    total = timedelta()
    for tt1, tt2 in date_list:
        local = tt2 - tt1
        total = total + local
        print(f"{hour_sec(tt1)} - {hour_sec(tt2)}  {local}   {total}")


def run():
    print("exemple : 8h40 9:00 16h40 16")
    date_list = []

    while True:
        print()
        add_date(date_list)
        print()
        show_diff(date_list)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)

"""
Prend des input

ex:
debut : 7h30
fin   : 10h30
duree : 3h

debut : 11h30
fin   : 12h00
duree : 3h30
"""
from datetime import datetime


def to_datetime(_str):
    try:
        return datetime.strptime(_str, "%Hh%M")
    except ValueError:
        try:
            return datetime.strptime(_str, "%H:%M")
        except ValueError:
            return datetime.strptime(_str, "%H")


def run():
    print("exemple :  8h40")
    print("           9:00")
    print("          16h40")
    print()

    debut = input("debut : ")
    d_debut = to_datetime(debut)

    fin = input("fin   : ")
    d_fin = to_datetime(fin)

    print("duree :", d_fin - d_debut)


if __name__ == "__main__":
    run()

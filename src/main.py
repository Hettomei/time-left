"""
Prend des input
"""

import argparse
from datetime import timedelta
from program_exception import UserException, ForceQuitException
from user_data import UserData
from utils import text_to_datetime, format_timedelta, format_timedelta2
import sys

FRIDAY = 4

def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Affiche un chrono",
    )

    parser.add_argument(
        "--append-to",
        "-a",
        dest="append_to",
        default="",
        help="Charge ce fichier, et écrit le resultat à la fin du fichier",
        metavar="/d/code/file.txt",
    )

    return parser.parse_args(args)


def init_data(user_data: UserData) -> None:
    if not user_data.append_to:
        print("Pas de fichier à charger")
        return

    user_data.load_file()

    if user_data.date_list:
        print()
        user_data.print_list()
        print()
    else:
        print("Pas de data à charger")


def read_input(user_data: UserData) -> None:
    debut = input("command ou debut : ").strip()
    # d: delete
    if debut == "d":
        if not user_data.delete_last():
            print("nothing to delete")
    # h: help
    elif debut == "h" or debut == "?":
        help_screen(user_data)
    # cd: change date
    elif debut == "cd" or debut == "c":
        relative = input("nouvelle date relative  (-1, -2 ...) : ").strip()
        user_data.change_date(relative)
        print(user_data)
    # q: quit
    elif debut == "q":
        raise ForceQuitException("q")
    elif debut == "rab" or debut == "r":
        rab_screen(user_data)
    # else: parse au mieux les data pour trouver une date
    else:
        d_debut = text_to_datetime(debut)
        fin = input("fin   : ")
        d_fin = text_to_datetime(fin)
        user_data.append(d_debut, d_fin)


def main_loop(user_data: UserData) -> None:
    print("h : affiche l'aide")
    while True:
        try:
            read_input(user_data)
        except UserException as e:
            print(f"ERROR {e}")

        user_data.print_list()
        print()

def print_rab(base_de_calcul: timedelta, fait: timedelta, rab_existant: timedelta) -> None:
    print(f"sur {format_timedelta2(base_de_calcul)} manque : {format_timedelta2(base_de_calcul)} - {format_timedelta2(fait)} = {format_timedelta2(base_de_calcul - fait)} donc ")
    print(f"rab: {format_timedelta2(rab_existant - (base_de_calcul - fait))}")
    print()

def rab_screen(user_data: UserData) -> None:
    print(f"""
rab : fait le calcul sur le rab

format :
-------
8h40, 8:40, 8 40, 8, 8m, 40s
""")
    if user_data.raw_rab:
        raw_rab = user_data.raw_rab
        print("rab disponible : " + raw_rab)
    else:
        raw_rab = input("rab disponible : ").strip()
    print()
    a = text_to_datetime(raw_rab)
    delta_rab = timedelta(hours=a.hour, minutes=a.minute, seconds=a.second)


    delta_en_cours = user_data.get_final_delta()

    delta_7h30 = timedelta(hours=7, minutes=30)
    delta_7h00 = timedelta(hours=7)
    if user_data.current_date.weekday() == FRIDAY:
        print_rab(delta_7h00, delta_en_cours, delta_rab)
    else:
        print_rab(delta_7h30, delta_en_cours, delta_rab)

def help_screen(user_data: UserData) -> None:
    print(f"""
commandes
---------
?,h   : affiche l'aide
d     : supprime la derniere ligne
c,cd  : change la date relative à la date du jour. ex: -1
r,rab : Affiche les different calcul de rab
q,C-c : quitte l'app

valeurs
-------
8h40, 8:40, 8 40, 8, 8m, 40s

data
----
{user_data}""")


def run(args) -> None:
    params = parse_args(args)
    user_data = UserData(params.append_to)
    init_data(user_data)

    try:
        main_loop(user_data)
    except (KeyboardInterrupt, ForceQuitException):
        user_data.write_in_file()


if __name__ == "__main__":
    run(sys.argv[1::1])

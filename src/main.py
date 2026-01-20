"""
Prend des input
"""

import argparse
from datetime import datetime, timedelta
from program_exception import UserException, ForceQuitException
from user_data import UserData
from utils import text_to_datetime
import sys


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="Affiche un chrono",
    )

    parser.add_argument(
        "--append-to",
        "-a",
        dest="append_to",
        default="",
        help="Au moment de quitter, ecris le resultat à la fin du fichier",
        metavar="/d/code/file.txt",
    )

    return parser.parse_args(args)


def read_input(user_data: UserData) -> None:
    debut = input("command : ").strip()
    # d: delete
    if debut == "d":
        if not user_data.delete_last():
            print("nothing to delete")
    # h: help
    elif debut == "h":
        help_screen(user_data)
    # cd: change date
    elif debut == "cd":
        relative = input("nouvelle date relative  (-1, -2 ...) : ").strip()
        user_data.change_date(relative)
        print(user_data)
    # q: quit
    elif debut == "q":
        raise ForceQuitException("q")
    # l: load file
    elif debut == "l":
        user_data.load_file()
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

        print(user_data.diff_to_string())
        print()


def help_screen(user_data: UserData) -> None:
    print(f"""
commandes
---------
h   : affiche l'aide
d   : supprime la derniere ligne
cd  : change la date relative à la date du jour. ex: -1
q
C-c : quitte l'app
l   : load file

valeurs
-------
8h40, 8:40, 8 40, 8, 8m, 40s

data
----
{user_data}""")


def run(args) -> None:
    params = parse_args(args)
    user_data = UserData(params.append_to)

    try:
        main_loop(user_data)
    except (KeyboardInterrupt, ForceQuitException):
        user_data.write_in_file()


if __name__ == "__main__":
    run(sys.argv[1::1])

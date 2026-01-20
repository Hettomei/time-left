"""
Prend des input
"""

import argparse
from datetime import datetime, timedelta
from program_exception import UserException, ForceQuitException
from user_data import UserData
import sys

# import os
# SEPARATOR = os.linesep
SEPARATOR: str = "\n"
# SEPARATOR = "\r\n"


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


def to_datetime(_str: str, pattern: str) -> datetime | None:
    try:
        return datetime.strptime(_str, pattern)
    except ValueError:
        return None


def text_to_datetime(_str: str) -> datetime:
    result = None
    str_time = _str.strip()
    for pattern in [
        "%Hh%Mm%Ss",
        "%H:%M:%S",
        "%H %M %S",
        "%Hh%Mm",
        "%Hh%M",
        "%H:%M",
        "%H %M",
        "%H",
        "%Hh",
        "%Mm",
        "%Ss",
    ]:
        result = to_datetime(str_time, pattern)
        if result:
            return result

    raise UserException(f"No date for {str_time}")


def read_input(user_data: UserData):
    debut = input("debut : ")
    # d: delete
    if debut.strip() == "d":
        if not user_data.delete_last():
            print("nothing to delete")
        return
    # h: help
    elif debut.strip() == "h":
        help_screen(user_data)
        return
    # cd: change date
    elif debut.strip() == "cd":
        relative = input("nouvelle date relative  (-1, -2 ...) : ")
        user_data.change_date(relative.strip())
        print(user_data)
        return
    # q: quit
    elif debut.strip() == "q":
        raise ForceQuitException("q")
        return

    d_debut = text_to_datetime(debut)

    fin = input("fin   : ")
    d_fin = text_to_datetime(fin)
    user_data.append(d_debut, d_fin)


def main_loop(user_data: UserData) -> None:
    while True:
        try:
            read_input(user_data)
        except UserException as e:
            print(f"ERROR {e}")
        print()
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

valeurs
-------
8h40, 8:40, 8 40, 8, 8m, 40s

data
----
{user_data}""")


def run(args) -> None:
    print("h : affiche l'aide")

    params = parse_args(args)
    user_data = UserData(params.append_to)

    try:
        main_loop(user_data)
    except (KeyboardInterrupt, ForceQuitException):
        user_data.write_in_file()


if __name__ == "__main__":
    run(sys.argv[1::1])

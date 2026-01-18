"""
Prend des input
"""

import argparse
from datetime import datetime, timedelta
import sys

# import os
# SEPARATOR = os.linesep
SEPARATOR = "\n"
# SEPARATOR = "\r\n"


class UserException(Exception):
    pass


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


def to_datetime(_str, pattern):
    try:
        return datetime.strptime(_str, pattern)
    except ValueError:
        return None


def text_to_datetime(_str):
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


def read_input(date_list):
    debut = input("debut : ")
    if debut.strip() == "d":
        if len(date_list) > 0:
            date_list.pop()
        else:
            print("nothing to delete")
        return
    elif debut.strip() == "h":
        help_screen()
        return

    d_debut = text_to_datetime(debut)

    fin = input("fin   : ")
    d_fin = text_to_datetime(fin)
    date_list.append([d_debut, d_fin])


def format_datetime(_datetime):
    return datetime.strftime(_datetime, "%H:%M:%S")


def format_timedelta(_timedelta):
    """
    si timedelta(hours=1)  => "01:00:00"
    si timedelta(hours=10) => "10:00:00"
    si timedelta(days=1, hours=1) => "1 day, 01:00:00"
    """
    if len(str(_timedelta)) < 8:
        return f"0{_timedelta}"
    if _timedelta.days > 0:
        a = str(_timedelta).split(", ")
        if len(str(a[1])) < 8:
            a[1] = f"0{a[1]}"

        return ", ".join(a)

    return str(_timedelta)


def diff_to_list(date_list):
    total = timedelta()
    lines = []
    for tt1, tt2 in date_list:
        if tt2 <= tt1:
            # On ajoute 24h
            tt2 = tt2 + timedelta(days=1)
        local = tt2 - tt1
        total = total + local
        lines.append(
            f"{format_datetime(tt1)} - {format_datetime(tt2)}  {format_timedelta(local)}  {format_timedelta(total)}"
        )

    return lines


def diff_to_string(date_list):
    return SEPARATOR.join(diff_to_list(date_list))


def main_loop(date_list):
    while True:
        try:
            read_input(date_list)
        except UserException as e:
            print(f"ERROR {e}")
        print()
        print(diff_to_string(date_list))
        print()


def append_to(params, date_list):
    if not params.append_to:
        print()
        print("Nothing saved")
        return None

    if not date_list:
        print()
        print("Nothing saved")
        return None

    with open(params.append_to, "a", encoding="utf-8", newline=SEPARATOR) as myfile:
        myfile.writelines(
            [
                SEPARATOR,
                datetime.strftime(datetime.now(), "# %Y-%m-%d %A"),
                SEPARATOR,
                SEPARATOR,
                diff_to_string(date_list),
                SEPARATOR,
                SEPARATOR,
            ]
        )

    print()
    print(f"Saved to {params.append_to}")
    return True


def help_screen():
    print("=============================")
    print("Exemple de valeurs possible :")
    print("8h40 , 8:40 , 8 40, 8")
    print("h : affiche l'aide")
    print("d : supprime la derniere ligne")
    print("=============================")


def run(args):
    params = parse_args(args)
    print("h : affiche l'aide")
    date_list = []

    try:
        main_loop(date_list)
    except KeyboardInterrupt:
        append_to(params, date_list)


if __name__ == "__main__":
    run(sys.argv[1::1])

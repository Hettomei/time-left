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


def to_datetime_full(_str):
    result = None
    str_time = _str.strip()
    for pattern in [
        "%Hh%M",
        "%H:%M",
        "%H %M",
        "%H",
        "%Hh",
    ]:
        result = to_datetime(str_time, pattern)
        if result:
            return result

    raise ValueError(f"No date for {str_time}")


def ask_date(date_list):
    debut = input("debut : ")
    if debut.strip() == "d":
        if len(date_list) > 0:
            date_list.pop()
        else:
            print("nothing to delete")
        return

    d_debut = to_datetime_full(debut)

    fin = input("fin   : ")
    d_fin = to_datetime_full(fin)
    date_list.append([d_debut, d_fin])


def hour_sec(_datetime):
    return datetime.strftime(_datetime, "%Hh%M")


def diff_to_list(date_list):
    total = timedelta()
    lines = []
    for tt1, tt2 in date_list:
        local = tt2 - tt1
        total = total + local
        lines.append(f"{hour_sec(tt1)} - {hour_sec(tt2)}  {local}   {total}")

    return lines


def diff_to_string(date_list):
    return SEPARATOR.join(diff_to_list(date_list))


def ask_time(date_list):
    while True:
        print()
        try:
            ask_date(date_list)
        except ValueError as e:
            print(e)
        print()
        print(diff_to_string(date_list))


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


def run(args):
    params = parse_args(args)
    print("exemple de valeurs possible : 8h40 , 8:40 , 8 40, 8")
    print("d : supprime la derniere ligne")
    date_list = []

    try:
        ask_time(date_list)
    except KeyboardInterrupt:
        append_to(params, date_list)
        sys.exit(0)


if __name__ == "__main__":
    run(sys.argv[1::1])

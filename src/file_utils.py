from utils import text_to_datetime, format_current_date

import re
from datetime import date, datetime, timedelta

SEPARATOR: str = "\n"

extract_delta = re.compile(r"^(\S+) - (\S+)")


def load_file(filepath: str, current_date: date):
    """
    Tente de charger les valeurs présente dans un fichier
    Cette fonction ne leve pas d erreur
    """
    initial_date_match = format_current_date(current_date)

    state = "nothing"
    date_list: list[list[datetime]] = []
    with open(filepath, "r", encoding="utf-8", newline=SEPARATOR) as f:
        for s_line in f:
            # d abord on cherche le titre de la section
            if state == "nothing" and s_line.rstrip() == initial_date_match:
                state = "found_date"
                continue

            # ensuite on cherche un timedelta
            if state == "found_date" and extract_delta.match(s_line.rstrip()):
                state = "found_datedelta"

            # Ici, toutes les lignes consecutive doivent matcher
            # sinon, on s arrete
            if state == "found_datedelta":
                # print("line: " + s_line.rstrip())
                deltas = extract_delta.match(s_line.rstrip())
                if deltas:
                    # print("g1:" + deltas.group(1) + " -- g2:" + deltas.group(2))
                    date_list.append(
                        [
                            text_to_datetime(deltas.group(1)),
                            text_to_datetime(deltas.group(2)),
                        ]
                    )
                else:
                    # plus rien a faire, on quitte la fonction
                    break

    return date_list


def overwrite(filepath: str, current_date: date, data: str):
    """
    si il trouve la ligne,
    réécrit à la place des lignes existantes
    sinon, l ajoute à la fin
    """
    with open(filepath, "a", encoding="utf-8", newline=SEPARATOR) as myfile:
        myfile.writelines(
            [
                SEPARATOR,
                SEPARATOR,
                format_current_date(current_date),
                SEPARATOR,
                SEPARATOR,
                data,
                SEPARATOR,
            ]
        )

    # on recherche la string, on la trouve

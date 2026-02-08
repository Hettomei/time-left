from utils import text_to_datetime, format_current_date
from program_exception import UserException

import re
from datetime import date, datetime, timedelta
from pathlib import Path
import tempfile, shutil

SEPARATOR: str = "\n"

extract_delta = re.compile(r"^(.+?) - (.+?) ")


def create_temporary_copy(path):
    with tempfile.NamedTemporaryFile(
        prefix="time_left_", suffix="_" + path.name, delete=False
    ) as tmp:
        shutil.copy2(path, tmp.name)
        return tmp.name


def load_file(filepath: Path, current_date: date):
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
                    try:
                        date_list.append(
                            [
                                text_to_datetime(deltas.group(1)),
                                text_to_datetime(deltas.group(2)),
                            ]
                        )
                    except UserException as ue:
                        print("Problem at <" + s_line.rstrip() + "> " + str(ue))

                else:
                    # plus rien a faire, on quitte la fonction
                    break

    return date_list


def write_data(target, date_title, data):
    """
    on ecrit le titre,
    on saute une ligne
    on ecrit les data
    on saute une ligne
    """
    target.write(date_title)
    target.write(SEPARATOR)
    target.write(SEPARATOR)
    for d in data:
        target.write(d)
        target.write(SEPARATOR)


def overwrite(targetfile: Path, current_date: date, data: str):
    """
    Copier le fichier
    prendre la copie et le lire
    prendre le fichier initiale
    ajouter ligne par ligne le fichier copié
    quand j arrive au point interessant, le remplacer
    remettre toute la fin

    sinon, l ajoute à la fin
    """
    copy__file = create_temporary_copy(targetfile)
    date_title = format_current_date(current_date)
    state = "nothing"
    print("save copy at " + copy__file)

    with (
        open(targetfile, "w", encoding="utf-8", newline=SEPARATOR) as target,
        open(copy__file, "r", encoding="utf-8", newline=SEPARATOR) as copy,
    ):
        for line in copy:
            # d abord on cherche le titre de la section
            if state == "nothing":
                if line.rstrip() == date_title:
                    state = "write_new_data"
                else:
                    target.write(line)

            if state == "write_new_data":
                write_data(target, date_title, data)
                state = "find_delta_or_copy_line"
                continue

            # ensuite on cherche un timedelta
            if state == "find_delta_or_copy_line":
                if extract_delta.match(line.rstrip()):
                    # tous les delta doivent etre consecutif, donc il faut un mode special
                    state = "delete_delta"
                elif line.rstrip():
                    # tout ce qui n est pas date et heure, on l ecrit
                    target.write(line)

            if state == "delete_delta":
                if extract_delta.match(line.rstrip()):
                    # print("delete: " + line.rstrip())
                    continue
                else:
                    # tous les delta doivent etre consecutif
                    # si on arrive ici, c est qu il n y en a plus
                    state = "continue_import"

            # A partir d ici, on copy tout
            if state == "continue_import":
                target.write(line)

        # si on arrive ici, c'est qu il n a pas trouvé de ligne, on ajoute
        if state == "nothing":
            write_data(target, date_title, data)

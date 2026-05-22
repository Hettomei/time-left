from utils import text_to_datetime, format_current_date
from program_exception import UserException

import re
from datetime import date, datetime, timedelta
from pathlib import Path
import tempfile, shutil

SEPARATOR: str = "\n"

extract_delta = re.compile(r"^(.+?) - (.+?) ")
extract_rab = re.compile(r"^rab: (.+?)$")


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
    raw_rab: str = None
    rab_data: str = None

    # create if didn t exist
    open(filepath, "a", encoding="utf-8").close()

    with open(filepath, "r", encoding="utf-8", newline=SEPARATOR) as f:
        for s_line in f:
            clean_line = s_line.rstrip()
            # on cherche le mot clef "rab" et on sauve la derniere ligne. toujours
            if state != "found_datedelta" and clean_line.startswith("rab: "):
                raw_rab = clean_line

            # d abord on cherche le titre de la section
            if state == "nothing" and clean_line == initial_date_match:
                state = "found_date"
                continue

            # ensuite on cherche un timedelta
            if state == "found_date" and extract_delta.match(clean_line):
                state = "found_datedelta"

            # Ici, toutes les lignes consecutive doivent matcher
            # sinon, on s arrete
            if state == "found_datedelta":
                # print("line: " + clean_line)
                deltas = extract_delta.match(clean_line)
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
                        print("Problem at <" + clean_line + "> " + str(ue))
                else:
                    # plus rien a faire, on quitte la fonction pour ne pas charger plus
                    break

    if raw_rab:
        rab_match = extract_rab.match(raw_rab)
        if rab_match:
            rab_data = rab_match.group(1)

    return date_list, rab_data


def write_data(target, date_title, data, new_rab):
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
    target.write(new_rab)
    target.write(SEPARATOR)


def overwrite(targetfile: Path, current_date: date, data, new_rab: str):
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
            clean_line = line.rstrip()
            # d abord on cherche le titre de la section
            if state == "nothing":
                if clean_line == date_title:
                    state = "write_new_data"
                else:
                    target.write(line)

            if state == "write_new_data":
                write_data(target, date_title, data, new_rab)
                state = "find_delta_or_copy_line"
                continue

            # ensuite on cherche un timedelta
            if state == "find_delta_or_copy_line":
                if extract_delta.match(clean_line):
                    # tous les delta doivent etre consecutif, donc il faut un mode special
                    state = "delete_delta"
                elif clean_line:
                    # tout ce qui n est pas date et heure, on l ecrit
                    target.write(line)

            if state == "delete_delta":
                if extract_delta.match(clean_line):
                    # print("delete: " + clean_line)
                    continue
                if clean_line.startswith("rab: "):
                    # print("delete: " + clean_line)
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
            write_data(target, date_title, data, new_rab)
            target.write(SEPARATOR)

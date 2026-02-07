from user_data import UserData
from utils import text_to_datetime
import re

SEPARATOR: str = "\n"

extract_delta = re.compile(r"^(\d\d:\d\d:\d\d) - (\d\d:\d\d:\d\d)")


def load_file(user_data: UserData):
    """
    Efface le contenu de user_data.date_list
    tente de charger avec les valeur.
    ne leve pas d erreur
    """
    user_data.clear_list()
    initial_date_match = user_data.format_current_date()

    state = "nothing"
    with open(user_data.append_to, "r", encoding="utf-8", newline=SEPARATOR) as f:
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
                deltas = extract_delta.match(s_line.rstrip())
                if deltas:
                    user_data.append(
                        text_to_datetime(deltas.group(1)),
                        text_to_datetime(deltas.group(2)),
                    )
                else:
                    # plus rien a faire, on quitte la fonction
                    return

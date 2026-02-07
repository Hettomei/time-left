from user_data import UserData
from utils import text_to_datetime
import re

SEPARATOR: str = "\n"

extract_delta = re.compile(r"^(\S+) - (\S+)")


def load_file(user_data: UserData):
    """
    tente de charger les valeurs.
    Si une valeur est trouvée :
    - efface le contenu de user_data.date_list
    - remplit avec les nouvelles data

    Cette fonction ne leve pas d erreur
    """
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
                user_data.clear_list()
                state = "found_datedelta"

            # Ici, toutes les lignes consecutive doivent matcher
            # sinon, on s arrete
            if state == "found_datedelta":
                # print("line: " + s_line.rstrip())
                deltas = extract_delta.match(s_line.rstrip())
                if deltas:
                    # print("g1:" + deltas.group(1) + " -- g2:" + deltas.group(2))
                    user_data.append(
                        text_to_datetime(deltas.group(1)),
                        text_to_datetime(deltas.group(2)),
                    )
                else:
                    # plus rien a faire, on quitte la fonction
                    return

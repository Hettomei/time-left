SEPARATOR: str = "\n"


def load_file(_file):
    """
    si pas de fichier :
        afficher "pas de fichier", ne rien faire
    si fichier et data chargeable :
        effacer le contenu de date_list puis le remplacer
    si fichier et data non chargeable :
        affiche le probleme
    """
    if not _file:
        return "pas de fichier"

    try:
        with open(_file, "r", encoding="utf-8", newline=SEPARATOR) as myfile:
            return "ok"
            # return myfile.read()

    except FileNotFoundError:
        return "fichier inexistant"

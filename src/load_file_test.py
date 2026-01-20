import tempfile
from utils import text_to_datetime
from load_file import load_file
from user_data import UserData


def test_load_file_when_no_file():
    assert load_file("") == "pas de fichier"


def test_load_file_when_file_does_not_exist():
    assert load_file("file") == "fichier inexistant"


def test_load_file_when_file_load_nothing():
    a = tempfile.NamedTemporaryFile(delete=False)
    u = UserData(a.name)
    u.append(text_to_datetime("8h"), text_to_datetime("9"))
    u.append(text_to_datetime("10m"), text_to_datetime("20m"))
    u.write_in_file()

    assert load_file(a.name) == "ok"

import tempfile
from utils import text_to_datetime
from file_utils import load_file
from user_data import UserData

import re


def test_load_file_when_date_but_no_data():
    pass


def test_load_file_when_file_load_data():
    a = tempfile.NamedTemporaryFile(delete=False)
    u = UserData(a.name)
    u.append(text_to_datetime("8h"), text_to_datetime("9"))
    u.append(text_to_datetime("10m"), text_to_datetime("20m"))
    u.write_in_file()

    u.clear_list()
    load_file(u)
    assert len(u.date_list) == 2

    assert u.date_list[0] == [text_to_datetime("8h"), text_to_datetime("9h")]
    assert u.date_list[1] == [text_to_datetime("10m"), text_to_datetime("20m")]

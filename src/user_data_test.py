"""
Test
"""

from user_data import UserData
from datetime import date, datetime, timedelta
from main import text_to_datetime

import tempfile


def test_change_date():
    user_data = UserData()
    assert user_data.current_date == date.today()

    user_data.change_date("  1 ")
    assert user_data.current_date == date.today() + timedelta(days=1)

    user_data.change_date("  -1 ")
    assert user_data.current_date == date.today()

    user_data.change_date("  -1 ")
    assert user_data.current_date == date.today() - timedelta(days=1)


def test_diff_to_list():
    user_data = UserData()
    t = text_to_datetime

    user_data.append(t("0h"), t("0 1"))
    user_data.append(t("1h"), t("1 59"))
    user_data.append(t("13:35"), t("13:35"))
    user_data.append(t("1"), t("1 3"))
    user_data.append(t("8"), t("18 7"))
    user_data.append(t("7 30"), t("18h20"))
    user_data.append(t("1"), t("4"))
    user_data.append(t("1"), t("4"))

    assert user_data.diff_to_list() == [
        "00h - 00h01  00:01:00  00:01:00",
        "01h - 01h59  00:59:00  01:00:00",
        "13h35 - 13h35  1 day, 00:00:00  1 day, 01:00:00",
        "01h - 01h03  00:03:00  1 day, 01:03:00",
        "08h - 18h07  10:07:00  1 day, 11:10:00",
        "07h30 - 18h20  10:50:00  1 day, 22:00:00",
        "01h - 04h  03:00:00  2 days, 01:00:00",
        "01h - 04h  03:00:00  2 days, 04:00:00",
    ]


def test_diff_to_list_v2():
    user_data = UserData()
    t = text_to_datetime
    user_data.append(t("18"), t("1"))
    user_data.append(t("15"), t("8"))
    assert user_data.diff_to_list() == [
        "18h - 01h  07:00:00  07:00:00",
        "15h - 08h  17:00:00  1 day, 00:00:00",
    ]


def test_load_file_when_file_load_data():
    a = tempfile.NamedTemporaryFile(delete=False)
    u = UserData(a.name)
    u.append(text_to_datetime("8h"), text_to_datetime("9"))
    u.append(text_to_datetime("10m"), text_to_datetime("20m"))
    u.write_in_file()

    u.clear_list()
    u.load_file()
    assert len(u.date_list) == 2

    assert u.date_list[0] == [text_to_datetime("8h"), text_to_datetime("9h")]
    assert u.date_list[1] == [text_to_datetime("10m"), text_to_datetime("20m")]

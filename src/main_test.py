"""
Test
"""

from datetime import datetime, timedelta

import main


def test_text_to_datetime():
    assert main.format_datetime(main.text_to_datetime("10")) == "10:00:00"
    assert main.format_datetime(main.text_to_datetime("11h")) == "11:00:00"
    assert main.format_datetime(main.text_to_datetime("11h32  ")) == "11:32:00"
    assert main.format_datetime(main.text_to_datetime("11 32")) == "11:32:00"
    assert main.format_datetime(main.text_to_datetime("    12    34  ")) == "12:34:00"
    assert main.format_datetime(main.text_to_datetime("    13:35  ")) == "13:35:00"
    assert main.text_to_datetime("    13:35  ") == datetime(
        1900, 1, 1, hour=13, minute=35
    )


def test_diff_to_list():
    date_list = []
    t = main.text_to_datetime

    date_list.append([t("0h"), t("0 1")])
    date_list.append([t("1h"), t("1 59")])
    date_list.append([t("13:35"), t("13:35")])
    date_list.append([t("1"), t("1 3")])
    date_list.append([t("8"), t("18 7")])
    date_list.append([t("7 30"), t("18h20")])
    date_list.append([t("1"), t("4")])
    date_list.append([t("1"), t("4")])

    assert main.diff_to_list(date_list) == [
        "00:00:00 - 00:01:00  00:01:00  00:01:00",
        "01:00:00 - 01:59:00  00:59:00  01:00:00",
        "13:35:00 - 13:35:00  1 day, 00:00:00  1 day, 01:00:00",
        "01:00:00 - 01:03:00  00:03:00  1 day, 01:03:00",
        "08:00:00 - 18:07:00  10:07:00  1 day, 11:10:00",
        "07:30:00 - 18:20:00  10:50:00  1 day, 22:00:00",
        "01:00:00 - 04:00:00  03:00:00  2 days, 01:00:00",
        "01:00:00 - 04:00:00  03:00:00  2 days, 04:00:00",
    ]


def test_full_integration_v2():
    date_list = []
    t = main.text_to_datetime
    date_list.append([t("18"), t("1")])
    date_list.append([t("15"), t("8")])
    print(main.diff_to_list(date_list))
    assert main.diff_to_list(date_list) == [
        "18:00:00 - 01:00:00  07:00:00  07:00:00",
        "15:00:00 - 08:00:00  17:00:00  1 day, 00:00:00",
    ]


def test_format_timedelta():
    assert main.format_timedelta(timedelta(hours=1)) == "01:00:00"
    assert main.format_timedelta(timedelta(hours=10)) == "10:00:00"
    assert main.format_timedelta(timedelta(hours=25)) == "1 day, 01:00:00"

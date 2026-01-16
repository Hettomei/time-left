"""
Test
"""
from datetime import datetime, timedelta

import main


def test_to_datetime_full():
    assert main.hour_sec(main.to_datetime_full("10")) == "10h00"
    assert main.hour_sec(main.to_datetime_full("11h")) == "11h00"
    assert main.hour_sec(main.to_datetime_full("11h32  ")) == "11h32"
    assert main.hour_sec(main.to_datetime_full("11 32")) == "11h32"
    assert main.hour_sec(main.to_datetime_full("    12    34  ")) == "12h34"
    assert main.hour_sec(main.to_datetime_full("    13:35  ")) == "13h35"


def test_full_integration():
    date_list = []
    t = main.to_datetime_full

    date_list.append([t("0h"), t("0")])
    date_list.append([t("13:35"), t("13:35")])
    date_list.append([t("1"), t("1 3")])
    date_list.append([t("8"), t("18 7")])
    date_list.append([t("7 30"), t("18h20")])
    date_list.append([t("1"), t("4")])
    date_list.append([t("1"), t("4")])

    assert main.diff_to_list(date_list) == [
            '00h00 - 00h00  00:00:00  00:00:00',
            '13h35 - 13h35  00:00:00  00:00:00',
            '01h00 - 01h03  00:03:00  00:03:00',
            '08h00 - 18h07  10:07:00  10:10:00',
            '07h30 - 18h20  10:50:00  21:00:00',
            '01h00 - 04h00  03:00:00  1 day, 00:00:00',
            '01h00 - 04h00  03:00:00  1 day, 03:00:00',
            ]


def test_full_integration_v2():
    date_list = []
    t = main.to_datetime_full
    date_list.append([t("18"), t("1")])
    date_list.append([t("15"), t("8")])
    assert main.diff_to_list(date_list) == [
            '18h00 - 01h00  07:00:00  07:00:00',
            '15h00 - 08h00  17:00:00  1 day, 00:00:00',
            ]

def test_format_timedelta():
    assert main.format_timedelta(timedelta(hours=1))  == "01:00:00"
    assert main.format_timedelta(timedelta(hours=10)) == "10:00:00"
    assert main.format_timedelta(timedelta(hours=25)) == "1 day, 01:00:00"

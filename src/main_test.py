"""
Test
"""

from datetime import datetime, timedelta
from user_data import UserData, format_datetime, format_timedelta

import main


def test_text_to_datetime():
    assert format_datetime(main.text_to_datetime("10")) == "10:00:00"
    assert format_datetime(main.text_to_datetime("11h")) == "11:00:00"
    assert format_datetime(main.text_to_datetime("11h32  ")) == "11:32:00"
    assert format_datetime(main.text_to_datetime("11 32")) == "11:32:00"
    assert format_datetime(main.text_to_datetime("    12    34  ")) == "12:34:00"
    assert format_datetime(main.text_to_datetime("    13:35  ")) == "13:35:00"
    assert main.text_to_datetime("    13:35  ") == datetime(
        1900, 1, 1, hour=13, minute=35
    )


def test_format_timedelta():
    assert format_timedelta(timedelta(hours=1)) == "01:00:00"
    assert format_timedelta(timedelta(hours=10)) == "10:00:00"
    assert format_timedelta(timedelta(hours=25)) == "1 day, 01:00:00"

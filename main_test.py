"""
Test
"""
import main

def test_to_datetime_full():
    assert main.hour_sec(main.to_datetime_full("10")) == "10h00"
    assert main.hour_sec(main.to_datetime_full("11h")) == "11h00"
    assert main.hour_sec(main.to_datetime_full("11h32  ")) == "11h32"
    assert main.hour_sec(main.to_datetime_full("11 32")) == "11h32"
    assert main.hour_sec(main.to_datetime_full("    12    34  ")) == "12h34"
    assert main.hour_sec(main.to_datetime_full("    13:35  ")) == "13h35"

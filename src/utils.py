from program_exception import UserException
from datetime import date, datetime, timedelta


def to_datetime(_str: str, pattern: str) -> datetime | None:
    try:
        return datetime.strptime(_str, pattern)
    except ValueError:
        return None


def format_current_date(current_date: date) -> str:
    return current_date.strftime("# %Y-%m-%d %A")


def format_datetime(_datetime: datetime) -> str:
    """
    Tous les formats doivent etre utilisable par text_to_datetime
    """
    if _datetime.second == 0:
        return datetime.strftime(_datetime, "%Hh%M")

    if _datetime.hour == 0 and _datetime.minute == 0:
        return datetime.strftime(_datetime, "%Ss")

    return datetime.strftime(_datetime, "%Hh%Mm%Ss")


def format_timedelta(_timedelta: timedelta) -> str:
    """
    si timedelta(hours=1)  => "01:00:00"
    si timedelta(hours=10) => "10:00:00"
    si timedelta(days=1, hours=1) => "1 day, 01:00:00"
    """
    if len(str(_timedelta)) < 8:
        return f"0{_timedelta}"
    if _timedelta.days > 0:
        a = str(_timedelta).split(", ")
        if len(str(a[1])) < 8:
            a[1] = f"0{a[1]}"

        return ", ".join(a)

    return str(_timedelta)


def text_to_datetime(_str: str) -> datetime:
    result = None
    str_time = _str.strip()
    for pattern in [
        "%Hh%Mm%Ss",
        "%H:%M:%S",
        "%H %M %S",
        "%Hh%Mm",
        "%Hh%M",
        "%H:%M",
        "%H %M",
        "%H",
        "%Hh",
        "%Mm",
        "%Ss",
    ]:
        result = to_datetime(str_time, pattern)
        if result:
            return result

    raise UserException(f"No date for {str_time}")

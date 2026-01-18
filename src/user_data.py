from datetime import date, datetime


class UserData:
    def __init__(self) -> None:
        self.current_date: date = date.today()
        self.date_list: list[datetime] = []

    def __str__(self) -> str:
        return f"UserData[{self.current_date}]"

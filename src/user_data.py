import file_utils

from datetime import date, datetime, timedelta
from utils import format_datetime, format_timedelta
from pathlib import Path

SEPARATOR: str = "\n"


class UserData:
    def __init__(self, append_to: str = "") -> None:
        self.append_to: str = append_to
        self.current_date: date = date.today()
        self.date_list: list[list[datetime]] = []

    def __str__(self) -> str:
        return f"UserData[{self.current_date}, file: {self.append_to}, date_list: {len(self.date_list)}]"

    def delete_last(self) -> bool:
        if len(self.date_list) > 0:
            self.date_list.pop()
            return True
        return False

    def append(self, d_debut: datetime, d_fin: datetime) -> None:
        self.date_list.append([d_debut, d_fin])

    def diff_to_list(self):
        total = timedelta()
        lines = []
        for tt1, tt2 in self.date_list:
            if tt2 <= tt1:
                # On ajoute 24h
                tt2 = tt2 + timedelta(days=1)
            local = tt2 - tt1
            total = total + local
            lines.append(
                f"{format_datetime(tt1)} - {format_datetime(tt2)}  {format_timedelta(local)}  {format_timedelta(total)}"
            )

        return lines

    def print_list(self) -> str:
        for l in self.diff_to_list():
            print(l)

    def load_file(self) -> None:
        if self.append_to:
            results = file_utils.load_file(Path(self.append_to), self.current_date)
            if results:
                self.date_list = results

    def write_in_file(self) -> None:
        """
        Si le fichier existe, réécrit à la place des
        lignes existantes
        """
        if not self.append_to:
            return

        if not self.date_list:
            print()
            print("Nothing to save")
            return

        print()
        file_utils.overwrite(
            Path(self.append_to), self.current_date, self.diff_to_list()
        )
        print(f"saved to {self.append_to}")

    def change_date(self, relative: str) -> None:
        """
        relative can be -1 to go back one day
        """
        change_days = int(relative)
        self.current_date = self.current_date + timedelta(days=change_days)
        self.load_file()

    def clear_list(self) -> None:
        self.date_list = []

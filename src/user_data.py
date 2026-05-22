import file_utils

from datetime import date, datetime, timedelta
from utils import text_to_datetime, format_datetime, format_timedelta, format_timedelta2, format_current_date
from pathlib import Path

SEPARATOR: str = "\n"
FRIDAY = 4

class UserData:
    def __init__(self, append_to: str = "") -> None:
        self.append_to: str = append_to
        self.current_date: date = date.today()
        self.date_list: list[list[datetime]] = []
        self.raw_rab: str = None

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

    def get_final_delta(self) -> timedelta:
        total = timedelta()
        lines = []
        for tt1, tt2 in self.date_list:
            if tt2 <= tt1:
                # On ajoute 24h
                tt2 = tt2 + timedelta(days=1)
            local = tt2 - tt1
            total = total + local

        return total

    def print_list(self) -> None:
        print(format_current_date(self.current_date))
        for l in self.diff_to_list():
            print(l)
        self.print_rab()


    def today_delta_rab(self) -> None:
        if self.current_date.weekday() == FRIDAY:
            return timedelta(hours=7)
        else:
            return timedelta(hours=7, minutes=30)


    def print_rab(self) -> None:
        if not self.raw_rab:
            return

        today_delta = self.today_delta_rab()
        print(f"rab avant: {self.raw_rab}, sur {format_timedelta2(today_delta)}, {self.new_rab()}");

    def new_rab(self) -> None:
        if not self.raw_rab:
            return ""

        a = text_to_datetime(self.raw_rab)
        delta_rab = timedelta(hours=a.hour, minutes=a.minute, seconds=a.second)
        today_delta = self.today_delta_rab()
        delta_en_cours = self.get_final_delta()

        return f"rab: {format_timedelta2(delta_rab - (today_delta - delta_en_cours))}"



    def load_file(self) -> None:
        if self.append_to:
            results, rab = file_utils.load_file(Path(self.append_to), self.current_date)
            if results:
                self.date_list = results
                self.raw_rab = rab

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
            Path(self.append_to), self.current_date, self.diff_to_list(), self.new_rab()
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

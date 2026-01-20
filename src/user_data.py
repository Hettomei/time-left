from datetime import date, datetime, timedelta
from load_file import load_file

SEPARATOR: str = "\n"


def format_datetime(_datetime: datetime) -> str:
    return datetime.strftime(_datetime, "%H:%M:%S")


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

    def diff_to_string(self) -> str:
        return SEPARATOR.join(self.diff_to_list())

    def write_in_file(self) -> None:
        if not self.append_to:
            print()
            print("Nothing saved")
            return

        if not self.date_list:
            print()
            print("Nothing to save")
            return

        with open(self.append_to, "a", encoding="utf-8", newline=SEPARATOR) as myfile:
            myfile.writelines(
                [
                    SEPARATOR,
                    self.current_date.strftime("# %Y-%m-%d %A"),
                    SEPARATOR,
                    SEPARATOR,
                    self.diff_to_string(),
                    SEPARATOR,
                    SEPARATOR,
                ]
            )

        print()
        print(f"Saved to {self.append_to}")

    def change_date(self, relative: str) -> None:
        a = int(relative)
        self.current_date = self.current_date + timedelta(days=a)

    def load_file(self) -> str:
        """
        si pas de fichier :
            afficher "pas de fichier", ne rien faire
        si fichier et data chargeable :
            effacer le contenu de date_list puis le remplacer
        si fichier et data non chargeable :
            affiche le probleme
        """
        return load_file(self.append_to)

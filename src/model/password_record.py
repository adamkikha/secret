from src.model.record import Record


class PasswordRecord(Record):
    def __init__(
        self,
        id: int,
        username: str,
        password: str,
        tag: str,
        url: str,
        notes: str,
        date: float,
    ):
        super().__init__(id, tag, notes, date)
        self.username = username
        self.password = password
        self.url = url
        self.pass_mdate = date
        self.warn = False

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def set_url(self, url: str):
        self.url = url

    def set_pass_mdate(self, date: float):
        self.pass_mdate = date

    def set_warn(self, warn: bool):
        self.warn = warn

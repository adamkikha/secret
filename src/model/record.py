import time


class Record:
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
        self.id = id
        self.username = username
        self.password = password
        self.tag = tag
        self.url = url
        self.notes = notes
        self.record_mdate = date
        self.pass_mdate = date

    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):
        self.password = password

    def set_tag(self, tag: str):
        self.tag = tag

    def set_url(self, url: str):
        self.url = url

    def set_notes(self, notes: str):
        self.notes = notes

    def set_mdate(self, date: float):
        self.record_mdate = date

    def set_pass_mdate(self, date: float):
        self.pass_mdate = date

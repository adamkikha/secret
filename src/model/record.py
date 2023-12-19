import time


class Record:
    def __init__(
        self, id: int, username: str, password: str, tag: str, url: str, notes: str
    ):
        self.id = id
        self.username = username
        self.password = password
        self.tag = tag
        self.url = url
        self.notes = notes
        now = time.localtime()
        self.record_mdate = now
        self.pass_mdate = now

    def __update_mdate__(self):
        self.record_mdate = time.localtime()

    def get_mdate(self, password: bool, readable: bool = False) -> str | float:
        """
        returns date as seconds since the epoch or in a readable format
        :param password: specify which date is needed (False for record mdate)
        :param readable: output readable format (default is False)
        :return: float or readable str
        """
        if password:
            date = self.pass_mdate
        else:
            date = self.record_mdate

        if readable:
            return time.strftime("%d/%m/%Y %H:%M:%S", date)
        else:
            return time.mktime(date)

    def set_username(self, username: str):
        self.username = username
        self.__update_mdate__()

    def set_password(self, password: str):
        self.password = password
        self.__update_mdate__()
        self.pass_mdate = self.record_mdate

    def set_tag(self, tag: str):
        self.tag = tag
        self.__update_mdate__()

    def set_url(self, url: str):
        self.url = url
        self.__update_mdate__()

    def set_notes(self, notes: str):
        self.notes = notes
        self.__update_mdate__()

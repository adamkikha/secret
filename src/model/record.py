class Record:
    def __init__(
        self,
        id: int,
        tag: str,
        notes: str,
        date: float,
    ):
        self.id = id
        self.tag = tag
        self.notes = notes
        self.record_mdate = date

    def set_tag(self, tag: str):
        self.tag = tag

    def set_notes(self, notes: str):
        self.notes = notes

    def set_mdate(self, date: float):
        self.record_mdate = date

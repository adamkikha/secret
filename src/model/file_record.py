from src.model.record import Record


class FileRecord(Record):
    def __init__(
        self, id: int, name: str, size: int, tag: str, notes: str, date: float
    ):
        super().__init__(id, tag, notes, date)
        self.name = name
        self.size = size

    def set_name(self, name: str):
        self.name = name

    def set_size(self, size: int):
        self.size = size

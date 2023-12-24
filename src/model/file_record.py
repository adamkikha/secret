from src.model.record import Record
import os


class FileRecord(Record):
    def __init__(
        self, id: int, path: str, size: int, tag: str, notes: str, date: float
    ):
        super().__init__(id, tag, notes, date)
        self.path = path
        self.name = os.path.basename(path)
        self.size = size

    def set_name(self, name: str):
        self.name = name

    def set_size(self, size: int):
        self.size = size

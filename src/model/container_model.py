from src.model.model import Model
from src.model.file_record import FileRecord
import pickle


class ContainerModel(Model):
    def __init__(self, time_oracle):
        super().__init__(time_oracle)
        self.file_data: list[bytes] = []

    def initialize(self, path: str, create: bool):
        super().initialize(path, create)
        self.file_data = []

    def construct_records(self, plaintext: bytes):
        self.records, self.file_data, self.next_id = pickle.loads(plaintext)
        self.view.update_data(self.get_records())

    def serialize_records(self):
        return pickle.dumps((self.records, self.file_data, self.next_id))

    def close_file(self):
        super().close_file()
        self.file_data = []

    def export_decrypted_file(self, id: int, path: str):
        file_index = self.__get_file_index__(id)
        with open(path, "wb") as file:
            file.write(self.file_data[file_index])

    def set_container_view(self, view):
        self.view = view

    def add_file_record(self, name: str, tag: str, notes: str):
        with open(name, "rb") as file:
            file_data = file.read()
        record = FileRecord(
            self.next_id,
            name,
            len(file_data),
            tag,
            notes,
            self.time_oracle.get_current_time(),
        )
        self.file_data.append(file_data)
        super().__add_record__(record)

    def delete_record(self, id: int):
        self.file_data.pop(self.__get_file_index__(id))
        return super().delete_record(id)

    def __get_file_index__(self, id: int):
        # get file record index
        return next(
            (i for i, record in enumerate(self.records) if record.id == id), None
        )

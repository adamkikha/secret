from src.model.model import Model
from src.model.file_record import FileRecord
import pickle
import os


class ContainerModel(Model):
    def __init__(self, time_oracle):
        super().__init__(time_oracle)
        self.file_data: list[bytes] = []
        self.filter = [None, None, None, None]
        self.search_term = ""

    def initialize(self, path: str, create: bool):
        super().initialize(path, create)
        self.file_data = []

    def construct_records(self, plaintext: bytes):
        self.records, self.file_data, self.next_id = pickle.loads(plaintext)
        self.update_data()

    def serialize_records(self):
        return pickle.dumps((self.records, self.file_data, self.next_id))

    def close_file(self):
        super().close_file()
        self.file_data = []

    def export_decrypted_file(self, id: int, path: str):
        file_index = self.__get_file_index__(id)
        record = self.get_record(id)
        file_path = os.path.join(path, record.name)
        with open(file_path, "wb") as file:
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

    def modify_file_record(self, id: int, name: str, tag: str, notes: str):
        modified = False
        record: FileRecord = self.get_record(id)
        if record.name != name:
            modified = True
            record.set_name(name)
        if record.tag != tag:
            modified = True
            record.set_tag(tag)
        if record.notes != notes:
            modified = True
            record.set_notes(notes)
        date = self.time_oracle.get_current_time()
        if modified:
            record.set_mdate(date)
            self.update_data()

    def filter_search(self, filter_list: list[str] = None, search_term: str = None):
        with self.update_data_lock:
            if filter_list is None:
                filter_list = self.filter
            else:
                self.filter = filter_list
            if search_term is None:
                search_term = self.search_term
            else:
                self.search_term = search_term
            result: list[FileRecord] = self.get_records().copy()

            for index, record in enumerate(result):
                if filter_list[0] and record.name != filter_list[0]:
                    result.pop(index)
                if filter_list[1] and record.size < int(filter_list[1]):
                    result.pop(index)
                if filter_list[2] and record.size > int(filter_list[2]):
                    result.pop(index)
                if filter_list[3] and record.tag != filter_list[3]:
                    result.pop(index)
                if search_term != "":
                    match = False
                    for value in (
                        record.name,
                        record.tag,
                        record.size,
                        record.notes,
                    ):
                        if search_term in value:
                            match = True
                            break
                    if not match:
                        result.pop(index)

            self.view.update_data(result)

    def delete_record(self, id: int):
        self.file_data.pop(self.__get_file_index__(id))
        return super().delete_record(id)

    def __get_file_index__(self, id: int):
        # get file record index
        return next(
            (i for i, record in enumerate(self.records) if record.id == id), None
        )

    def update_data(self):
        self.filter_search()

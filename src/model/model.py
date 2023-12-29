import pickle
from src.model.record import Record


class Model:
    def __init__(self):
        self.records: list[Record] = []
        self.next_id: int = 0
        self.path: str = ""
        self.view = None

    def initialize(self, path: str, create: bool):
        self.path = path
        self.records = []
        self.next_id = 0

        if create is True:
            # create a new file and close it
            open(path, "wb").close()
        else:
            with open(path, "rb") as file:
                self.ciphertext, self.tag, self.nonce, self.salt = pickle.loads(
                    file.read()
                )

    def construct_records(self, plaintext: bytes):
        self.records, self.next_id = pickle.loads(plaintext)
        self.update_data()

    def get_records(self):
        return self.records

    def get_record(self, id: int):
        for record in self.records:
            if record.id == id:
                return record
        return None

    def __add_record__(self, record: Record):
        self.records.append(record)
        self.next_id += 1
        self.update_data()

    def delete_record(self, id: int):
        for index in range(len(self.records)):
            if self.records[index].id == id:
                self.records.pop(index)
                self.update_data()
                return True
        return None

    def serialize_records(self):
        return pickle.dumps((self.records, self.next_id))

    def save_file(self, ciphertext: bytes, tag: bytes, nonce: bytes, salt: bytes):
        file_data = pickle.dumps((ciphertext, tag, nonce, salt))
        with open(self.path, "wb") as file:
            file.write(file_data)

    def close_file(self):
        self.path = ""
        self.records = []
        self.next_id = 0
        self.update_data()

    def update_data(self):
        self.view.update_data(self.get_records())

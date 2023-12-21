import pickle
from src.model.record import Record
from src.utils import TimeOracle


class SecretPass:
    def __init__(self, time_oracle: TimeOracle):
        self.time_oracle: TimeOracle = time_oracle
        self.records: list[Record] = []
        self.next_id: int = 0
        self.path: str = ""

    def initialize(self, path: str, create: bool):
        self.path = path
        self.records = []
        self.next_id = 0

        if create is True:
            # create a new file and close it
            open(path, "x").close()
        else:
            with open(path, "rb") as file:
                self.ciphertext, self.tag, self.nonce = pickle.loads(file.read())

    def construct_records(self, plaintext: bytes):
        self.records, self.next_id = pickle.loads(plaintext)

    def get_records(self):
        return self.records

    def get_record(self, id: int):
        for record in self.records:
            if record.id == id:
                return record
        return None

    def add_record(self, record: Record):
        self.records.append(record)
        self.next_id += 1

    def delete_record(self, id: int):
        for index in range(len(self.records)):
            if self.records[index].id == id:
                self.records.pop(index)
                return True
        return None

    def serialize_records(self):
        return pickle.dumps((self.records, self.next_id))

    def save_file(self, ciphertext: bytes, tag: bytes, nonce: bytes):
        file_data = pickle.dumps((ciphertext, tag, nonce))
        with open(self.path, "wb") as file:
            file.write(file_data)

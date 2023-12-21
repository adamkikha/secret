import os
import pickle
import pytest
from src.model.passwords_model import PasswordsModel
from src.model.record import Record
from src.utils import TimeOracle


class Test_PasswordsModel:
    time_oracle = TimeOracle()
    passwords_model = PasswordsModel(time_oracle)

    def test_records(self):
        self.passwords_model.initialize("test1.secretpass", create=True)
        tests = [
            (0, "a", "1", "t", "n.com", "a1b2c3", self.time_oracle.get_current_time()),
            (
                1,
                "b",
                "2",
                "a",
                "e.net",
                "testtest",
                self.time_oracle.get_current_time(),
            ),
            (
                2,
                "c",
                "3",
                "g",
                "s.net",
                "lorem ipsum",
                self.time_oracle.get_current_time(),
            ),
            (
                3,
                "d",
                "4",
                "s",
                "w.net",
                "@#u9nrf$M",
                self.time_oracle.get_current_time(),
            ),
        ]

        test_records = []
        for test in tests:
            test_records.append(Record(*test))

        print(test_records)
        # add records
        for record in test_records:
            print(record)
            counter = self.passwords_model.next_id
            length = len(self.passwords_model.get_records())
            self.passwords_model.add_record(record)
            assert self.passwords_model.next_id == counter + 1 == length + 1
            assert self.passwords_model.get_records()[length].id == record.id

        # get records
        for record in test_records:
            assert self.passwords_model.get_record(record.id) is record

        # delete records
        for record in test_records:
            length = len(self.passwords_model.get_records())
            assert self.passwords_model.delete_record(record.id) is True
            assert self.passwords_model.get_record(record.id) is None
            assert len(self.passwords_model.get_records()) == length - 1

        os.remove("test1.secretpass")

    def test_files(self):
        self.passwords_model.initialize("test1.secretpass", create=True)
        self.passwords_model.add_record(
            Record(
                self.passwords_model.next_id,
                "a",
                "1",
                "t",
                "n.com",
                "a1b2c3",
                self.time_oracle.get_current_time(),
            )
        )
        self.passwords_model.add_record(
            Record(
                self.passwords_model.next_id,
                "b",
                "2",
                "a",
                "e.net",
                "testtest",
                self.time_oracle.get_current_time(),
            )
        )
        records = self.passwords_model.get_records()
        next_id = self.passwords_model.next_id
        # serialize , save file and load
        self.passwords_model.save_file(
            self.passwords_model.serialize_records(),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        self.passwords_model = PasswordsModel(self.time_oracle)
        self.passwords_model.initialize("test1.secretpass", create=False)
        assert self.passwords_model.tag == b"\x55\x55"
        assert self.passwords_model.nonce == b"\x12\x34"
        assert self.passwords_model.salt == b"\x01\xAB"
        assert self.passwords_model.ciphertext == pickle.dumps((records, next_id))

        # construct records
        self.passwords_model.construct_records(self.passwords_model.ciphertext)
        assert self.passwords_model.next_id == next_id
        assert len(self.passwords_model.get_records()) == len(records)
        for old_record, new_record in zip(records, self.passwords_model.get_records()):
            assert old_record.id == new_record.id
            assert old_record.username == new_record.username
            assert old_record.password == new_record.password
            assert old_record.tag == new_record.tag
            assert old_record.url == new_record.url
            assert old_record.notes == new_record.notes
            assert old_record.record_mdate == new_record.record_mdate
            assert old_record.pass_mdate == new_record.pass_mdate

        # initiation
        with pytest.raises(FileNotFoundError):
            self.passwords_model = PasswordsModel(self.time_oracle)
            self.passwords_model.initialize("test2.secretpass", create=False)

        with pytest.raises(FileExistsError):
            self.passwords_model = PasswordsModel(self.time_oracle)
            self.passwords_model.initialize("test1.secretpass", create=True)

        os.remove("test1.secretpass")

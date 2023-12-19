import os
import pickle
import pytest
from src.model.secretpass import SecretPass
from src.model.record import Record


class Test_SecretPass:
    sp = SecretPass("test1.secretpass", True)

    def test_records(self):
        tests = [
            Record(0, "a", "1", "t", "n.com", "a1b2c3"),
            Record(1, "b", "2", "a", "e.net", "testtest"),
            Record(2, "c", "3", "g", "s.net", "lorem ipsum"),
            Record(3, "d", "4", "s", "w.net", "@#u9nrf$M"),
        ]

        # add records
        for record in tests:
            counter = self.sp.next_id
            length = len(self.sp.get_records())
            self.sp.add_record(record)
            assert self.sp.next_id == counter + 1 == length + 1
            assert self.sp.get_records()[length].id == record.id

        # get records
        for record in tests:
            assert self.sp.get_record(record.id) is record

        # delete records
        for record in tests:
            length = len(self.sp.get_records())
            assert self.sp.delete_record(record.id) is True
            assert self.sp.get_record(record.id) is None
            assert len(self.sp.get_records()) == length - 1

    def test_files(self):
        self.sp.add_record(Record(self.sp.next_id, "a", "1", "t", "n.com", "a1b2c3"))
        self.sp.add_record(Record(self.sp.next_id, "b", "2", "a", "e.net", "testtest"))
        records = self.sp.get_records()
        next_id = self.sp.next_id

        # serialize , save file and load
        self.sp.save_file(self.sp.serialize_records(), b"\x55\x55", b"\x12\x34")
        self.sp = SecretPass("test1.secretpass")
        assert self.sp.tag == b"\x55\x55"
        assert self.sp.nonce == b"\x12\x34"
        assert self.sp.ciphertext == pickle.dumps((records, next_id))

        # construct records
        self.sp.construct_records(self.sp.ciphertext)
        assert self.sp.next_id == next_id
        assert len(self.sp.get_records()) == len(records)
        for old_record, new_record in zip(records, self.sp.get_records()):
            assert old_record.id == new_record.id
            assert old_record.username == new_record.username
            assert old_record.password == new_record.password
            assert old_record.tag == new_record.tag
            assert old_record.url == new_record.url
            assert old_record.notes == new_record.notes
            assert old_record.get_mdate(False) == old_record.get_mdate(False)
            assert old_record.get_mdate(True) == old_record.get_mdate(True)

        # initiation
        with pytest.raises(FileNotFoundError):
            self.sp = SecretPass("test2.secretpass")

        with pytest.raises(FileExistsError):
            self.sp = SecretPass("test1.secretpass", True)

        os.remove("test1.secretpass")

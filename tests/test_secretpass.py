import os
import pickle
import pytest
from src.model.secretpass import SecretPass
from src.model.record import Record
from src.utils import TimeOracle


class Test_SecretPass:
    time_oracle = TimeOracle()
    sp = SecretPass(time_oracle)
    sp.initialize("test1.secretpass", create=True)

    def test_records(self):
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
            counter = self.sp.next_id
            length = len(self.sp.get_records())
            self.sp.add_record(record)
            assert self.sp.next_id == counter + 1 == length + 1
            assert self.sp.get_records()[length].id == record.id

        # get records
        for record in test_records:
            assert self.sp.get_record(record.id) is record

        # delete records
        for record in test_records:
            length = len(self.sp.get_records())
            assert self.sp.delete_record(record.id) is True
            assert self.sp.get_record(record.id) is None
            assert len(self.sp.get_records()) == length - 1

    def test_files(self):
        self.sp.add_record(
            Record(
                self.sp.next_id,
                "a",
                "1",
                "t",
                "n.com",
                "a1b2c3",
                self.time_oracle.get_current_time(),
            )
        )
        self.sp.add_record(
            Record(
                self.sp.next_id,
                "b",
                "2",
                "a",
                "e.net",
                "testtest",
                self.time_oracle.get_current_time(),
            )
        )
        records = self.sp.get_records()
        next_id = self.sp.next_id

        # serialize , save file and load
        self.sp.save_file(self.sp.serialize_records(), b"\x55\x55", b"\x12\x34")
        self.sp = SecretPass(self.time_oracle)
        self.sp.initialize("test1.secretpass", create=False)
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
            assert old_record.record_mdate == new_record.record_mdate
            assert old_record.pass_mdate == new_record.pass_mdate

        # initiation
        with pytest.raises(FileNotFoundError):
            self.sp = SecretPass(self.time_oracle)
            self.sp.initialize("test2.secretpass", create=False)

        with pytest.raises(FileExistsError):
            self.sp = SecretPass(self.time_oracle)
            self.sp.initialize("test1.secretpass", create=True)

        os.remove("test1.secretpass")

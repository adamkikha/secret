import os
import pickle
import pytest
from src.model.passwords_model import PasswordsModel
from src.utils import TimeOracle
from copy import copy
from src.view.view import View


class Test_PasswordsModel:
    time_oracle = TimeOracle()
    passwords_model = PasswordsModel(time_oracle)
    passwords_model.set_passwords_view(View().passwords_view)

    def test_records(self):
        self.passwords_model.initialize("test1.secretpass", create=True)
        tests = [
            (0, "a", "1", "t", "n.com", "a1b2c3"),
            (1, "b", "2", "a", "e.net", "testtest"),
            (2, "c", "3", "g", "s.net", "lorem ipsum"),
            (
                3,
                "d",
                "4",
                "s",
                "w.net",
                "@#u9nrf$M",
            ),
        ]

        # add records
        for record in tests:
            counter = self.passwords_model.next_id
            length = len(self.passwords_model.get_records())
            self.passwords_model.add_pass_record(*record[1:6])
            assert self.passwords_model.next_id == counter + 1 == length + 1
            assert self.passwords_model.get_records()[length].id == record[0]

        # get records
        for record in tests:
            assert self.passwords_model.get_record(record[0]).id == record[0]

        # modify records
        test_records = self.passwords_model.get_records()
        copy_test_records = test_records.copy()

        old_record, new_record = test_records[1], copy_test_records[2]
        original_record = copy(old_record)
        self.passwords_model.modify_pass_record(
            old_record.id,
            new_record.username,
            old_record.password,
            old_record.tag,
            old_record.url,
            old_record.notes,
        )
        assert old_record.record_mdate > original_record.record_mdate
        assert old_record.pass_mdate == original_record.pass_mdate
        assert old_record.username == new_record.username
        assert old_record.password == original_record.password
        assert old_record.tag == original_record.tag
        assert old_record.url == original_record.url
        assert old_record.notes == original_record.notes

        old_record, new_record = test_records[2], copy_test_records[3]
        original_record = copy(old_record)
        self.passwords_model.modify_pass_record(
            old_record.id,
            old_record.username,
            old_record.password,
            old_record.tag,
            old_record.url,
            old_record.notes,
        )
        assert old_record.record_mdate == original_record.record_mdate
        assert old_record.pass_mdate == original_record.pass_mdate
        assert old_record.username == original_record.username
        assert old_record.password == original_record.password
        assert old_record.tag == original_record.tag
        assert old_record.url == original_record.url
        assert old_record.notes == original_record.notes

        old_record, new_record = test_records[0], copy_test_records[1]
        self.passwords_model.modify_pass_record(
            old_record.id,
            new_record.username,
            new_record.password,
            new_record.tag,
            new_record.url,
            new_record.notes,
        )
        assert old_record.record_mdate > original_record.record_mdate
        assert old_record.pass_mdate > original_record.pass_mdate
        assert old_record.username == new_record.username
        assert old_record.password == new_record.password
        assert old_record.tag == new_record.tag
        assert old_record.url == new_record.url
        assert old_record.notes == new_record.notes

        # delete records
        for record in test_records:
            length = len(self.passwords_model.get_records())
            assert self.passwords_model.delete_record(record.id) is True
            assert self.passwords_model.get_record(record.id) is None
            assert len(self.passwords_model.get_records()) == length - 1

        os.remove("test1.secretpass")

    def test_files(self):
        self.passwords_model.initialize("test1.secretpass", create=True)
        self.passwords_model.add_pass_record(
            "a",
            "1",
            "t",
            "n.com",
            "a1b2c3",
        )
        self.passwords_model.add_pass_record(
            "b",
            "2",
            "a",
            "e.net",
            "testtest",
        )
        records = self.passwords_model.get_records().copy()
        next_id = self.passwords_model.next_id
        # serialize , save file and load
        self.passwords_model.save_file(
            self.passwords_model.serialize_records(),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
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

        # close file
        self.passwords_model.close_file()
        assert self.passwords_model.path == ""
        assert len(self.passwords_model.records) == 0
        assert self.passwords_model.next_id == 0

        # initiation
        with pytest.raises(FileNotFoundError):
            self.passwords_model.initialize("test2.secretpass", create=False)

        # check overwrite
        self.passwords_model.initialize("test1.secretpass", create=True)

        os.remove("test1.secretpass")

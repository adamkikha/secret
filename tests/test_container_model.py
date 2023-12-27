import os
import pickle
import random

import pytest
from src.model.container_model import ContainerModel
from src.utils import TimeOracle
from src.view.view import View
from copy import copy
from src.model.file_record import FileRecord


class Test_ContainerModel:
    time_oracle = TimeOracle()
    container_model = ContainerModel(time_oracle)
    container_model.set_container_view(View().container_view)

    def test_records(self):
        self.container_model.initialize("test.cont", create=True)
        open("a", "x").close()
        open("b", "x").close()
        open("c", "x").close()
        open("d", "x").close()
        tests = [
            (0, "a", "t", "a1b2c3"),
            (1, "b", "a", "testtest"),
            (2, "c", "g", "lorem ipsum"),
            (3, "d", "s", "@#u9nrf$M"),
        ]

        # add records
        for record in tests:
            counter = self.container_model.next_id
            length = len(self.container_model.get_records())
            self.container_model.add_file_record(*record[1:4])
            assert self.container_model.next_id == counter + 1 == length + 1
            assert (
                len(self.container_model.file_data)
                == len(self.container_model.get_records())
                == length + 1
            )
            assert self.container_model.get_records()[length].id == record[0]

        # get records
        for record in tests:
            assert self.container_model.get_record(record[0]).id == record[0]
            assert (
                self.container_model.get_records()[
                    self.container_model.__get_file_index__(record[0])
                ].id
                == record[0]
            )

        # modify records
        test_records = self.container_model.get_records()
        copy_test_records = test_records.copy()

        old_record, new_record = test_records[1], copy_test_records[2]
        original_record = copy(old_record)
        self.container_model.modify_file_record(
            old_record.id,
            new_record.name,
            old_record.tag,
            old_record.notes,
        )
        assert old_record.record_mdate > original_record.record_mdate
        assert old_record.name == new_record.name
        assert old_record.tag == original_record.tag
        assert old_record.notes == original_record.notes
        assert old_record.size == original_record.size

        old_record, new_record = test_records[2], copy_test_records[3]
        original_record = copy(old_record)
        self.container_model.modify_file_record(
            old_record.id,
            old_record.name,
            old_record.tag,
            old_record.notes,
        )
        assert old_record.record_mdate == original_record.record_mdate
        assert old_record.name == original_record.name
        assert old_record.tag == original_record.tag
        assert old_record.notes == original_record.notes
        assert old_record.size == original_record.size

        old_record, new_record = test_records[0], copy_test_records[1]
        self.container_model.modify_file_record(
            old_record.id,
            new_record.name,
            new_record.tag,
            new_record.notes,
        )
        assert old_record.record_mdate != original_record.record_mdate
        assert old_record.name == new_record.name
        assert old_record.tag == new_record.tag
        assert old_record.notes == new_record.notes
        assert old_record.size == original_record.size

        # delete records
        for record in tests:
            length = len(self.container_model.get_records())
            assert self.container_model.delete_record(record[0]) is True
            assert self.container_model.get_record(record[0]) is None
            assert self.container_model.__get_file_index__(record[0]) is None
            assert (
                len(self.container_model.get_records())
                == len(self.container_model.file_data)
                == length - 1
            )

        os.remove("test.cont")
        os.remove("a")
        os.remove("b")
        os.remove("c")
        os.remove("d")

    def test_files(self):
        tests = [
            ("a\ndata\ndata", "a", "t", "a1b2c3"),
            (
                "Proin bibendum libero quam, ullamcorper luctus magna viverra nec.\n"
                + "Mauris bibendum ex quam\n"
                + "Fusce non Cras ullamcorper cursus tincidunt\n"
                + "Curabitur a cursus quam, at egestas nisi\n"
                + "Nam dignissim, libero at.",
                "b",
                "a",
                "testtest",
            ),
        ]
        self.container_model.initialize("test", create=True)
        assert self.container_model.path == "test.cont"
        for test in tests:
            with open(test[1], "w") as test_file:
                test_file.write(test[0])
            self.container_model.add_file_record(*test[1:])
            os.remove(test[1])

        records = self.container_model.get_records().copy()
        file_data = self.container_model.file_data.copy()
        next_id = self.container_model.next_id

        # serialize , save file and load
        self.container_model.save_file(
            self.container_model.serialize_records(),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        self.container_model.initialize("test.cont", create=False)
        assert self.container_model.tag == b"\x55\x55"
        assert self.container_model.nonce == b"\x12\x34"
        assert self.container_model.salt == b"\x01\xAB"
        assert self.container_model.ciphertext == pickle.dumps(
            (records, file_data, next_id)
        )

        # construct records
        self.container_model.construct_records(self.container_model.ciphertext)
        assert self.container_model.next_id == next_id
        assert len(self.container_model.get_records()) == len(records)
        assert len(self.container_model.file_data) == len(file_data)
        for old_record, new_record in zip(records, self.container_model.get_records()):
            assert old_record.id == new_record.id
            assert old_record.name == new_record.name
            assert old_record.tag == new_record.tag
            assert old_record.size == new_record.size
            assert old_record.notes == new_record.notes
            assert old_record.record_mdate == new_record.record_mdate

        for old_data, new_data in zip(file_data, self.container_model.file_data):
            assert old_data == new_data

        # export decrypted file
        for record in self.container_model.get_records():
            self.container_model.export_decrypted_file(record.id, os.getcwd())
            with open(record.name, "r") as test_file:
                assert (
                    test_file.read()
                    == tests[self.container_model.__get_file_index__(record.id)][0]
                )

        # close file
        self.container_model.close_file()
        assert self.container_model.path == ""
        assert len(self.container_model.records) == 0
        assert len(self.container_model.file_data) == 0
        assert self.container_model.next_id == 0

        # initiation
        with pytest.raises(FileNotFoundError):
            self.container_model.initialize("test2.cont", create=False)

        # check overwrite
        self.container_model.initialize("test.cont", create=True)

        os.remove("test.cont")
        os.remove("a")
        os.remove("b")

    def test_filter_search(self):
        self.container_model.initialize("test.cont", create=True)
        with open("tests/file_test_records", "r") as records_file:
            lines = records_file.readlines()
            for line in lines:
                data = line.split(sep=" | ")
                self.container_model.__add_record__(
                    FileRecord(
                        self.container_model.next_id,
                        data[0],
                        int(data[1]),
                        data[2],
                        data[3],
                        random.randint(0, 1703632802),
                    )
                )

        # test filtering
        self.container_model.filter_search(["resume.pdf", "", "", ""], "")
        assert len(self.container_model.view.container_dec_data) == 2
        for record in self.container_model.view.container_dec_data:
            assert record.name == "resume.pdf"
        self.container_model.filter_search(["", "80000000", "", "Music"], "")
        assert len(self.container_model.view.container_dec_data) == 1
        for record in self.container_model.view.container_dec_data:
            assert record.name == "music2.flac"
            assert record.size > 9000000
            assert record.tag == "Music"
        self.container_model.filter_search(["", "", "", "Audio"], "")
        assert len(self.container_model.view.container_dec_data) == 2
        for record in self.container_model.view.container_dec_data:
            assert record.tag == "Audio"

        # test searching
        self.container_model.filter_search(["", "", "57000", ""], "create")
        assert len(self.container_model.view.container_dec_data) == 2
        for record in self.container_model.view.container_dec_data:
            assert record.size < 57000
            match = False
            for value in (
                record.name,
                record.tag,
                record.notes,
            ):
                if "create" in value:
                    match = True
                    break
            assert match is True
        self.container_model.filter_search(["", "56000000", "57000000", ""], ".mp4")
        assert len(self.container_model.view.container_dec_data) == 1
        record = self.container_model.view.container_dec_data[0]
        assert ".mp4" in record.name
        assert record.size == 56789012
        os.remove("test.cont")

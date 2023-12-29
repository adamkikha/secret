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
    time_oracle.set_model(passwords_model)
    passwords_model.set_passwords_view(View().passwords_view)

    def test_records(self):
        self.passwords_model.initialize("test1.pass", create=True)
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

        os.remove("test1.pass")

    def test_files(self):
        self.passwords_model.initialize("test1", create=True)
        assert self.passwords_model.path == "test1.pass"
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
        settings = copy(self.passwords_model.settings)
        next_id = self.passwords_model.next_id
        # serialize , save file and load
        self.passwords_model.save_file(
            self.passwords_model.serialize_records(),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        self.passwords_model.initialize("test1.pass", create=False)
        assert self.passwords_model.tag == b"\x55\x55"
        assert self.passwords_model.nonce == b"\x12\x34"
        assert self.passwords_model.salt == b"\x01\xAB"
        assert self.passwords_model.ciphertext == pickle.dumps(
            (records, settings, next_id)
        )

        # construct records
        self.passwords_model.construct_records(self.passwords_model.ciphertext)
        assert self.passwords_model.next_id == next_id
        assert len(self.passwords_model.get_records()) == len(records)

        old_settings = settings
        new_settings = self.passwords_model.settings
        assert old_settings.warn == new_settings.warn
        assert old_settings.warn_age == new_settings.warn_age
        assert old_settings.saved_version_count == new_settings.saved_version_count
        assert old_settings.lower_case == new_settings.lower_case
        assert old_settings.upper_case == new_settings.upper_case
        assert old_settings.digits == new_settings.digits
        assert old_settings.symbols == new_settings.symbols
        assert old_settings.length == new_settings.length

        for old_record, new_record in zip(records, self.passwords_model.get_records()):
            assert old_record.id == new_record.id
            assert old_record.username == new_record.username
            assert old_record.password == new_record.password
            assert old_record.tag == new_record.tag
            assert old_record.url == new_record.url
            assert old_record.notes == new_record.notes
            assert old_record.record_mdate == new_record.record_mdate
            assert old_record.pass_mdate == new_record.pass_mdate

        # backups
        old_dir = os.listdir()
        self.passwords_model.set_saved_version_count_setting(1)
        self.passwords_model.save_file(
            pickle.dumps(
                (
                    self.passwords_model.records,
                    self.passwords_model.settings,
                    self.passwords_model.next_id,
                )
            ),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        assert old_dir == os.listdir()

        self.passwords_model.set_saved_version_count_setting(3)
        self.passwords_model.save_file(
            pickle.dumps(
                (
                    records,
                    self.passwords_model.settings,
                    self.passwords_model.next_id,
                )
            ),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        self.passwords_model.save_file(
            pickle.dumps(
                (
                    records,
                    self.passwords_model.settings,
                    self.passwords_model.next_id,
                )
            ),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        self.passwords_model.save_file(
            pickle.dumps(
                (
                    records,
                    self.passwords_model.settings,
                    self.passwords_model.next_id,
                )
            ),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        assert old_dir != os.listdir()
        assert "test1_backups" in os.listdir()
        backups = os.listdir("test1_backups")
        assert len(backups) == 2
        settings = self.passwords_model.settings
        next_id = self.passwords_model.next_id

        # close file
        self.passwords_model.close_file()
        assert self.passwords_model.path == ""
        assert len(self.passwords_model.records) == 0
        assert self.passwords_model.filter == [None, None, None]
        assert self.passwords_model.search_term == ""
        assert self.passwords_model.next_id == 0

        # initiation
        with pytest.raises(FileNotFoundError):
            self.passwords_model.initialize("test2.pass", create=False)

        # check proper save after close
        self.passwords_model.initialize("test1.pass", create=False)
        self.passwords_model.construct_records(
            pickle.dumps(
                (
                    records,
                    settings,
                    next_id,
                )
            )
        )
        self.passwords_model.save_file(
            pickle.dumps(
                (
                    records,
                    settings,
                    next_id,
                )
            ),
            b"\x55\x55",
            b"\x12\x34",
            b"\x01\xAB",
        )
        new_backups = os.listdir("test1_backups")
        assert new_backups != backups
        assert len(new_backups) == 2
        for version in new_backups:
            os.remove(os.path.join("test1_backups", version))
        os.rmdir("test1_backups")
        os.remove("test1.pass")

        # check overwrite
        self.passwords_model.initialize("test1.pass", create=True)

    def test_settings(self):
        self.passwords_model.initialize("test1.pass", create=True)
        assert self.passwords_model.settings.warn is True
        assert self.passwords_model.settings.warn_age == 90
        assert self.passwords_model.settings.saved_version_count == 1
        assert self.passwords_model.settings.lower_case is True
        assert self.passwords_model.settings.upper_case is True
        assert self.passwords_model.settings.digits is True
        assert self.passwords_model.settings.symbols is True
        assert self.passwords_model.settings.length == 26

        self.passwords_model.set_warn_setting(True)
        assert self.passwords_model.settings.warn is True

        self.passwords_model.set_warn_age_setting(1)
        assert self.passwords_model.settings.warn_age == 1

        self.passwords_model.set_saved_version_count_setting(3)
        assert self.passwords_model.settings.saved_version_count == 3

        self.passwords_model.set_lower_case_setting(True)
        assert self.passwords_model.settings.lower_case is True

        self.passwords_model.set_upper_case_setting(False)
        assert self.passwords_model.settings.upper_case is False

        self.passwords_model.set_digits_setting(True)
        assert self.passwords_model.settings.digits is True

        self.passwords_model.set_symbols_setting(False)
        assert self.passwords_model.settings.symbols is False

        self.passwords_model.set_length_setting(10)
        assert self.passwords_model.settings.length == 10

        os.remove("test1.pass")

    def test_filter_search(self):
        self.passwords_model.initialize("test.pass", create=True)
        # adding test records
        with open("tests/password_test_records", "r") as records_file:
            lines = records_file.readlines()
            for line in lines:
                data = line.split(sep=" | ")
                self.passwords_model.add_pass_record(*data)

        # test filtering
        self.passwords_model.filter_search(["henry_cavill", "", ""], "")
        assert len(self.passwords_model.view.passwords_dec_data) == 2
        for record in self.passwords_model.view.passwords_dec_data:
            assert record.username == "henry_cavill"
        self.passwords_model.filter_search(["", "Music", ""], "")
        assert len(self.passwords_model.view.passwords_dec_data) == 3
        for record in self.passwords_model.view.passwords_dec_data:
            assert record.tag == "Music"
        self.passwords_model.filter_search(["", "Acting", "https://www.imdb.com"], "")
        assert len(self.passwords_model.view.passwords_dec_data) == 7
        for record in self.passwords_model.view.passwords_dec_data:
            assert record.tag == "Acting" and record.url == "https://www.imdb.com"

        # test searching
        self.passwords_model.filter_search(["", "Acting", ""], "on")
        assert len(self.passwords_model.view.passwords_dec_data) == 4
        for record in self.passwords_model.view.passwords_dec_data:
            assert record.tag == "Acting"
            match = False
            for value in (
                record.username,
                record.password,
                record.tag,
                record.url,
                record.notes,
            ):
                if "on" in value:
                    match = True
                    break
            assert match is True
        self.passwords_model.filter_search(["", "", ""], "de")
        assert len(self.passwords_model.view.passwords_dec_data) == 4
        for record in self.passwords_model.view.passwords_dec_data:
            match = False
            for value in (
                record.username,
                record.password,
                record.tag,
                record.url,
                record.notes,
            ):
                if "de" in value:
                    match = True
                    break
            assert match is True

        os.remove("test.pass")

from src.controller.passwords_controller import PasswordsController
from src.model.passwords_model import PasswordsModel
from src.utils import TimeOracle
from copy import copy
import os
import random
import string
from src.view.view import View


class Test_PasswordsController:
    time_oracle = TimeOracle()
    model = PasswordsModel(time_oracle)
    model.set_passwords_view(View().passwords_view)
    pass_controller = PasswordsController()
    pass_controller.set_passwords_model(model)
    success_tests = [
        ("pass123", "test1.pass"),
        ("rockyou", "test2.pass"),
    ]
    fail_tests = [
        ("wrongpass", "test1.pass"),
        ("yourock", "test2.pass"),
        ("pass123", "test3.pass"),
    ]

    def test_create_file(self, clean_up=True):
        for test in self.success_tests:
            self.pass_controller.create_file(*test)
            if clean_up:
                os.remove(test[1])

    def test_open_file(self):
        self.test_create_file(clean_up=False)
        for test in self.fail_tests:
            assert self.pass_controller.open_file(*test) is False

        for test in self.success_tests:
            assert self.pass_controller.open_file(*test) is True
            os.remove(test[1])

    def test_save_file(self):
        self.test_create_file(clean_up=False)
        assert self.pass_controller.save_file() is True
        self.pass_controller.close_file(save=False)
        assert self.pass_controller.save_file() is False
        for test in self.success_tests:
            os.remove(test[1])

    def test_add_modify_delete(self):
        self.pass_controller.create_file(*self.success_tests[0])
        tests = [
            (0, "a", "1", "t", "n.com", "a1b2c3"),
            (
                1,
                "b",
                "2",
                "a",
                "e.net",
                "testtest",
            ),
            (2, "c", "3", "g", "s.net", "lorem ipsum"),
            (3, "d", "4", "s", "w.net", "@#u9nrf$M"),
        ]

        # add records
        for test in tests:
            counter = self.pass_controller.model.next_id
            length = len(self.pass_controller.model.get_records())
            self.pass_controller.add_record(*test[1:6])
            assert self.pass_controller.model.next_id == counter + 1 == length + 1
            assert self.pass_controller.model.get_records()[length].id == test[0]

        test_records = self.pass_controller.model.get_records()
        # modify records
        copy_test_records = test_records.copy()

        old_record, new_record = test_records[1], copy_test_records[2]
        original_record = copy(old_record)
        self.pass_controller.modify_record(
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
        self.pass_controller.modify_record(
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
        self.pass_controller.modify_record(
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
            length = len(self.pass_controller.model.get_records())
            assert self.pass_controller.delete_record(record.id) is True
            assert self.pass_controller.model.get_record(record.id) is None
            assert len(self.pass_controller.model.get_records()) == length - 1

        os.remove(self.success_tests[0][1])

    def test_password_generator(self):
        # Test 1: Only lower case letters
        self.pass_controller.set_lower_case_setting(True)
        self.pass_controller.set_upper_case_setting(False)
        self.pass_controller.set_digits_setting(False)
        self.pass_controller.set_symbols_setting(False)
        self.pass_controller.set_length_setting(10)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert any(char in string.ascii_lowercase for char in password) is True
            assert any(char in string.ascii_uppercase for char in password) is False
            assert any(char in string.digits for char in password) is False
            assert any(char in string.punctuation for char in password) is False
            assert len(password) == 10

        # Test 2: Only upper case letters
        self.pass_controller.set_lower_case_setting(False)
        self.pass_controller.set_upper_case_setting(True)
        self.pass_controller.set_digits_setting(False)
        self.pass_controller.set_symbols_setting(False)
        self.pass_controller.set_length_setting(15)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert any(char in string.ascii_lowercase for char in password) is False
            assert any(char in string.ascii_uppercase for char in password) is True
            assert any(char in string.digits for char in password) is False
            assert any(char in string.punctuation for char in password) is False
            assert len(password) == 15

        # Test 3: Only digits
        self.pass_controller.set_lower_case_setting(False)
        self.pass_controller.set_upper_case_setting(False)
        self.pass_controller.set_digits_setting(True)
        self.pass_controller.set_symbols_setting(False)
        self.pass_controller.set_length_setting(20)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert any(char in string.ascii_lowercase for char in password) is False
            assert any(char in string.ascii_uppercase for char in password) is False
            assert any(char in string.digits for char in password) is True
            assert any(char in string.punctuation for char in password) is False
            assert len(password) == 20

        # Test 4: Only symbols
        self.pass_controller.set_lower_case_setting(False)
        self.pass_controller.set_upper_case_setting(False)
        self.pass_controller.set_digits_setting(False)
        self.pass_controller.set_symbols_setting(True)
        self.pass_controller.set_length_setting(26)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert any(char in string.ascii_lowercase for char in password) is False
            assert any(char in string.ascii_uppercase for char in password) is False
            assert any(char in string.digits for char in password) is False
            assert any(char in string.punctuation for char in password) is True
            assert len(password) == 26

        # Test : lower_case letters and digits
        self.pass_controller.set_lower_case_setting(True)
        self.pass_controller.set_upper_case_setting(False)
        self.pass_controller.set_digits_setting(True)
        self.pass_controller.set_symbols_setting(False)
        self.pass_controller.set_length_setting(30)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert (
                any(char in string.ascii_lowercase for char in password)
                or any(char in string.digits for char in password) is True
            )
            assert any(char in string.ascii_uppercase for char in password) is False
            assert any(char in string.punctuation for char in password) is False
            assert len(password) == 30

        # Test : upper_case letters and symbols
        self.pass_controller.set_lower_case_setting(False)
        self.pass_controller.set_upper_case_setting(True)
        self.pass_controller.set_digits_setting(False)
        self.pass_controller.set_symbols_setting(True)
        self.pass_controller.set_length_setting(32)

        random.seed(42)
        for _ in range(10):
            password = self.pass_controller.generate_password()
            assert (
                any(char in string.ascii_uppercase for char in password)
                or any(char in string.punctuation for char in password) is True
            )
            assert any(char in string.ascii_lowercase for char in password) is False
            assert any(char in string.digits for char in password) is False
            assert len(password) == 32

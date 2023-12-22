import os
from src.controller.controller import Controller
from src.model.passwords_model import PasswordsModel
from src.utils import TimeOracle
from src.view.view import Secret


class TestController:
    time_oracle = TimeOracle()
    model = PasswordsModel(time_oracle)
    model.set_passwords_view(Secret())
    controller = Controller()
    controller.set_model(model)
    success_tests = [
        ("pass123", "test1.secretpass"),
        ("rockyou", "test2.secretpass"),
    ]
    fail_tests = [
        ("wrongpass", "test1.secretpass"),
        ("yourock", "test2.secretpass"),
        ("pass123", "test3.secretpass"),
    ]

    def test_create_file(self, clean_up=True):
        for test in self.success_tests:
            self.controller.create_file(*test)
            if clean_up:
                os.remove(test[1])

    def test_open_file(self):
        self.test_create_file(clean_up=False)
        for test in self.fail_tests:
            assert self.controller.open_file(*test) is False

        for test in self.success_tests:
            assert self.controller.open_file(*test) is True
            os.remove(test[1])

    def test_save_file(self):
        self.test_create_file(clean_up=False)
        assert self.controller.save_file() is True
        self.controller.close_file(save=False)
        assert self.controller.save_file() is False
        for test in self.success_tests:
            os.remove(test[1])

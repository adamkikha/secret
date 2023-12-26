from src.controller.container_controller import ContainerController
from src.model.container_model import ContainerModel
from src.utils import TimeOracle
from copy import copy
import os
from src.view.view import View, ContainerView


class Test_ContainerController:
    time_oracle = TimeOracle()
    model = ContainerModel(time_oracle)
    model.set_container_view(View().container_view)
    cont_controller = ContainerController()
    cont_controller.set_container_model(model)
    success_tests = [
        ("pass123", "test1.cont"),
        ("rockyou", "test2.cont"),
    ]
    fail_tests = [
        ("wrongpass", "test1.cont"),
        ("yourock", "test2.cont"),
        ("pass123", "test3.cont"),
    ]

    def test_create_file(self, clean_up=True):
        for test in self.success_tests:
            self.cont_controller.create_file(*test)
            if clean_up:
                os.remove(test[1])

    def test_open_file(self):
        self.test_create_file(clean_up=False)
        for test in self.fail_tests:
            assert self.cont_controller.open_file(*test) is False

        for test in self.success_tests:
            assert self.cont_controller.open_file(*test) is True
            os.remove(test[1])

    def test_save_file(self):
        self.test_create_file(clean_up=False)
        assert self.cont_controller.save_file() is True
        self.cont_controller.close_file(save=False)
        assert self.cont_controller.save_file() is False
        for test in self.success_tests:
            os.remove(test[1])

    def test_add_modify_delete(self):
        self.cont_controller.create_file(*self.success_tests[0])
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
        for test in tests:
            counter = self.cont_controller.model.next_id
            length = len(self.cont_controller.model.get_records())
            self.cont_controller.add_file(*test[1:])
            assert self.cont_controller.model.next_id == counter + 1 == length + 1
            assert self.cont_controller.model.get_records()[length].id == test[0]

        test_records = self.cont_controller.model.get_records()

        # modify records
        copy_test_records = test_records.copy()

        old_record, new_record = test_records[1], copy_test_records[2]
        original_record = copy(old_record)
        self.cont_controller.modify_record(
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
        self.cont_controller.modify_record(
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
        self.cont_controller.modify_record(
            old_record.id,
            new_record.name,
            new_record.tag,
            new_record.notes,
        )
        assert old_record.record_mdate > original_record.record_mdate
        assert old_record.name == new_record.name
        assert old_record.tag == new_record.tag
        assert old_record.notes == new_record.notes
        assert old_record.size == original_record.size

        # delete records
        for record in test_records:
            length = len(self.cont_controller.model.get_records())
            assert self.cont_controller.delete_record(record.id) is True
            assert self.cont_controller.model.get_record(record.id) is None
            assert len(self.cont_controller.model.get_records()) == length - 1

        os.remove(self.success_tests[0][1])
        os.remove("a")
        os.remove("b")
        os.remove("c")
        os.remove("d")

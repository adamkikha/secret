from src.controller.passwords_controller import PasswordsController
from src.model.passwords_model import PasswordsModel
from src.utils import TimeOracle
from copy import copy
import os
from src.view.view import Secret


def test_passwords_controller():
    pass_controller = PasswordsController()
    time_oracle = TimeOracle()
    pass_controller.set_model(PasswordsModel(time_oracle))
    pass_controller.model.set_passwords_view(Secret())
    pass_controller.model.initialize("test.secretpass", True)
    tests = [
        (0, "a", "1", "t", "n.com", "a1b2c3", time_oracle.get_current_time()),
        (
            1,
            "b",
            "2",
            "a",
            "e.net",
            "testtest",
            time_oracle.get_current_time(),
        ),
        (
            2,
            "c",
            "3",
            "g",
            "s.net",
            "lorem ipsum",
            time_oracle.get_current_time(),
        ),
        (
            3,
            "d",
            "4",
            "s",
            "w.net",
            "@#u9nrf$M",
            time_oracle.get_current_time(),
        ),
    ]

    # add records
    for test in tests:
        counter = pass_controller.model.next_id
        length = len(pass_controller.model.get_records())
        pass_controller.add_record(*test[1:6])
        assert pass_controller.model.next_id == counter + 1 == length + 1
        assert pass_controller.model.get_records()[length].id == test[0]

    test_records = pass_controller.model.get_records()
    # modify records
    copy_test_records = test_records.copy()

    old_record, new_record = test_records[1], copy_test_records[2]
    original_record = copy(old_record)
    pass_controller.modify_record(
        old_record.id,
        new_record.username,
        old_record.password,
        old_record.tag,
        old_record.url,
        old_record.notes,
    )
    assert old_record.pass_mdate == original_record.pass_mdate
    assert old_record.username == new_record.username
    assert old_record.password == original_record.password
    assert old_record.tag == original_record.tag
    assert old_record.url == original_record.url
    assert old_record.notes == original_record.notes

    old_record, new_record = test_records[2], copy_test_records[3]
    original_record = copy(old_record)
    pass_controller.modify_record(
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
    pass_controller.modify_record(
        old_record.id,
        new_record.username,
        new_record.password,
        new_record.tag,
        new_record.url,
        new_record.notes,
    )
    assert old_record.username == new_record.username
    assert old_record.password == new_record.password
    assert old_record.tag == new_record.tag
    assert old_record.url == new_record.url
    assert old_record.notes == new_record.notes

    # delete records
    for record in test_records:
        length = len(pass_controller.model.get_records())
        assert pass_controller.delete_record(record.id) is True
        assert pass_controller.model.get_record(record.id) is None
        assert len(pass_controller.model.get_records()) == length - 1

    os.remove("test.secretpass")

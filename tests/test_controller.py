import pytest
from src.controller.controller import Controller


def test_password_entropy():
    # [(password, expected_entropy),..]
    tests = [
        (
            "123",
            4.75488,
        ),
        (
            "P4$$word",
            22.45884,
        ),
        (
            "0000000000000",
            0.00000,
        ),
        (
            "Abracadabra",
            28.43459,
        ),
        (
            "abraCadaBra",
            28.43459,
        ),
        (
            "acegikmoqsuwy",
            48.10572,
        ),
        (
            "89673460696657893304",
            60.00000,
        ),
        (
            "77starTrek-sta®w@rs!$",
            79.95445,
        ),
        (
            "t3XKczXFIOrqHRr_",
            60.91768,
        ),
        (
            "t3XKczXFIOrqHRr_t3XKczXFIOrqHRr",
            118.02800,
        ),
        (
            '+wq)tIw6gb4]Uh@"-E(=',
            84.95855,
        ),
        (
            'zK_f7M\\(#"W-?4AyN6g}',
            86.43856,
        ),
        (
            "hyevwfzfgyrlyafozwatdhujxlyltfdr",
            130.79881,
        ),
        (
            "1e3e4f50f8f7fe42a27d5d21ebc36af7",
            125.02050,
        ),
        (
            "111oo1o11oo1o1ooo1oo111oo11o1oooo1o11111",
            40.00000,
        ),
    ]
    for password, expected_entropy in tests:
        computed_entropy = Controller.get_password_entropy(password)
        assert computed_entropy == pytest.approx(expected_entropy, abs=0.00001)

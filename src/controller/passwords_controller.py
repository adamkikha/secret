import string
import secrets
from src.controller.controller import Controller


class PasswordsController(Controller):
    def set_passwords_model(self, model):
        self.model = model

    def add_record(self, username: str, password: str, tag: str, url: str, notes: str):
        self.model.add_pass_record(username, password, tag, url, notes)

    def modify_record(
        self, id: int, username: str, password: str, tag: str, url: str, notes: str
    ):
        self.model.modify_pass_record(id, username, password, tag, url, notes)

    def generate_password(self):
        (
            lower_case,
            upper_case,
            digits,
            symbols,
            length,
        ) = self.model.get_password_settings()

        character_set = ""
        if lower_case:
            character_set += string.ascii_lowercase
        if upper_case:
            character_set += string.ascii_uppercase
        if digits:
            character_set += string.digits
        if symbols:
            character_set += string.punctuation

        return "".join(secrets.choice(character_set) for _ in range(length))

    def set_warn_setting(self, state: bool):
        self.model.set_warn_setting(state)

    def set_warn_age_setting(self, age: int):
        self.model.set_warn_age_setting(age)

    def set_saved_version_count_setting(self, count: int):
        self.model.set_saved_version_count_setting(count)

    def set_lower_case_setting(self, state: bool):
        self.model.set_lower_case_setting(state)

    def set_upper_case_setting(self, state: bool):
        self.model.set_upper_case_setting(state)

    def set_digits_setting(self, state: bool):
        self.model.set_digits_setting(state)

    def set_symbols_setting(self, state: bool):
        self.model.set_symbols_setting(state)

    def set_length_setting(self, length: int):
        self.model.set_length_setting(length)

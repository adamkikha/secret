from src.controller.controller import Controller
from src.model.password_record import PasswordRecord


class PasswordsController(Controller):
    def add_record(self, username: str, password: str, tag: str, url: str, notes: str):
        record = PasswordRecord(
            self.model.next_id,
            username,
            password,
            tag,
            url,
            notes,
            self.model.time_oracle.get_current_time(),
        )
        self.model.add_record(record)

    def delete_record(self, id: int):
        return self.model.delete_record(id) == True

    def modify_record(
        self, id: int, username: str, password: str, tag: str, url: str, notes: str
    ):
        self.model.modify_pass_record(id, username, password, tag, url, notes)

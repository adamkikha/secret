from src.controller.controller import Controller


class PasswordsController(Controller):
    def set_passwords_model(self, model):
        self.model = model

    def add_record(self, username: str, password: str, tag: str, url: str, notes: str):
        self.model.add_pass_record(username, password, tag, url, notes)

    def delete_record(self, id: int):
        return self.model.delete_record(id) == True

    def modify_record(
        self, id: int, username: str, password: str, tag: str, url: str, notes: str
    ):
        self.model.modify_pass_record(id, username, password, tag, url, notes)

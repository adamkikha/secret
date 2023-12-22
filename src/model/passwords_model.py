from src.model.model import Model
from src.model.password_record import PasswordRecord


class PasswordsModel(Model):
    def modify_pass_record(
        self, id: int, username: str, password: str, tag: str, url: str, notes: str
    ):
        modified = False
        record: PasswordRecord = self.get_record(id)
        if record.username != username:
            modified = True
            record.set_username(username)
        if record.tag != tag:
            modified = True
            record.set_tag(tag)
        if record.url != url:
            modified = True
            record.set_url(url)
        if record.notes != notes:
            modified = True
            record.set_notes(notes)
        date = self.time_oracle.get_current_time()
        if record.password != password:
            modified = True
            record.set_password(password)
            record.set_pass_mdate(date)
        if modified:
            record.set_mdate(date)
            self.view.update_data(self.get_records())

    def set_passwords_view(self, view):
        self.view = view

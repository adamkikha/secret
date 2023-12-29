import os
import threading
from src.model.model import Model
from src.model.password_record import PasswordRecord
from src.model.password_settings import PasswordSettings
import pickle


class PasswordsModel(Model):
    def __init__(self, time_oracle):
        super().__init__()
        self.time_oracle = time_oracle
        self.settings = PasswordSettings()
        self.filter = [None, None, None]
        self.search_term = ""
        self.update_data_lock = threading.Lock()

    def initialize(self, path: str, create: bool):
        file_name, ext = os.path.splitext(path)
        if ext != ".pass":
            path = path + ".pass"
        super().initialize(path, create)
        self.settings = PasswordSettings()
        self.view.update_settings(self.settings)
        self.filter = [None, None, None]
        self.search_term = ""

    def construct_records(self, plaintext: bytes):
        self.records, self.settings, self.next_id = pickle.loads(plaintext)
        self.view.update_settings(self.settings)
        self.update_data()

    def serialize_records(self):
        return pickle.dumps((self.records, self.settings, self.next_id))

    def close_file(self):
        super().close_file()
        self.settings = PasswordSettings()
        self.view.update_settings(self.settings)
        self.filter = [None, None, None]
        self.search_term = ""

    def save_file(self, ciphertext: bytes, tag: bytes, nonce: bytes, salt: bytes):
        file_data = pickle.dumps((ciphertext, tag, nonce, salt))
        with open(self.path, "wb") as file:
            file.write(file_data)
        if self.settings.saved_version_count > 1:
            readable_date = self.time_oracle.get_readable_time(
                self.time_oracle.get_current_time()
            ).replace(":", "-")
            dir_name, file_name = os.path.split(self.path)
            base_name, ext = os.path.splitext(file_name)
            backup_directory = os.path.join(dir_name, base_name + "_backups")
            os.makedirs(backup_directory, exist_ok=True)
            counter = 0
            append_name = ""
            backups = os.listdir(backup_directory)
            while os.path.isfile(
                os.path.join(
                    backup_directory,
                    f"{base_name}_{readable_date}{append_name}" + ext,
                )
            ):
                counter += 1
                append_name = f"_{counter}"

            new_file_path = os.path.join(
                backup_directory, f"{base_name}_{readable_date}{append_name}" + ext
            )
            with open(new_file_path, "wb") as file:
                file.write(file_data)

            if len(backups) >= self.settings.saved_version_count - 1:
                backups.sort(
                    key=lambda f: os.path.getmtime(os.path.join(backup_directory, f))
                )
                os.remove(
                    os.path.join(
                        backup_directory,
                        backups.pop(-(self.settings.saved_version_count - 1)),
                    )
                )

    def set_warn_setting(self, setting: bool):
        self.settings.warn = setting
        self.view.update_settings(self.settings)
        for record in self.get_records():
            record.set_warn(False)

    def set_warn_age_setting(self, setting: int):
        self.settings.warn_age = setting
        self.view.update_settings(self.settings)

    def set_saved_version_count_setting(self, setting: int):
        self.settings.saved_version_count = setting
        self.view.update_settings(self.settings)

    def set_lower_case_setting(self, setting: bool):
        self.settings.lower_case = setting
        self.view.update_settings(self.settings)

    def set_upper_case_setting(self, setting: bool):
        self.settings.upper_case = setting
        self.view.update_settings(self.settings)

    def set_symbols_setting(self, setting: bool):
        self.settings.symbols = setting
        self.view.update_settings(self.settings)

    def set_digits_setting(self, setting: bool):
        self.settings.digits = setting
        self.view.update_settings(self.settings)

    def set_length_setting(self, setting: int):
        self.settings.length = setting
        self.view.update_settings(self.settings)

    def get_password_settings(self):
        return (
            self.settings.lower_case,
            self.settings.upper_case,
            self.settings.digits,
            self.settings.symbols,
            self.settings.length,
        )

    def add_pass_record(
        self, username: str, password: str, tag: str, url: str, notes: str
    ):
        record = PasswordRecord(
            self.next_id,
            username,
            password,
            tag,
            url,
            notes,
            self.time_oracle.get_current_time(),
        )
        self.records.append(record)
        self.next_id += 1
        self.update_data()

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
            record.set_warn(False)
        if modified:
            record.set_mdate(date)
            self.update_data()

    def set_passwords_view(self, view):
        self.view = view
        self.settings = PasswordSettings()
        self.view.update_settings(self.settings)

    def filter_search(self, filter_list: list[str] = None, search_term: str = None):
        with self.update_data_lock:
            self.__check_warn__()
            if filter_list is None:
                filter_list = self.filter
            else:
                self.filter = filter_list
            if search_term is None:
                search_term = self.search_term
            else:
                self.search_term = search_term
            result: list[PasswordRecord] = self.get_records().copy()

            for record in self.get_records():
                if filter_list[0] and record.username != filter_list[0]:
                    result.remove(record)
                elif filter_list[1] and record.tag != filter_list[1]:
                    result.remove(record)
                elif filter_list[2] and record.url != filter_list[2]:
                    result.remove(record)
                elif search_term != "":
                    match = False
                    for value in (
                        record.username,
                        record.password,
                        record.tag,
                        record.url,
                        record.notes,
                    ):
                        if search_term in value:
                            match = True
                            break
                    if not match:
                        result.remove(record)

            self.view.update_data(result)

    def __check_warn__(self):
        if self.settings.warn:
            current_time = self.time_oracle.get_current_time()
            for record in self.get_records():
                if (current_time - record.pass_mdate) >= (
                    self.settings.warn_age * 24 * 60 * 60
                ):
                    record.set_warn(True)

    def update_data(self):
        self.filter_search()

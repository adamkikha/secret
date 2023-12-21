import pytest
from src.model.password_record import PasswordRecord
from src.utils import TimeOracle


class Test_PasswordRecord:
    time_oracle = TimeOracle()
    pass_record = PasswordRecord(
        1,
        "abcd",
        "1234",
        "work",
        "www.website.com",
        "the quick brown fox jumps over the lazy dog",
        time_oracle.get_current_time(),
    )

    @pytest.mark.skip(
        reason="Initial call to function may be later than class creation by more than 2 seconds"
    )
    def test_get_mdate(self, pass_mdate: bool):
        assert (
            0
            <= self.time_oracle.get_current_time() - self.pass_record.record_mdate
            <= 2
        )
        if pass_mdate:
            assert self.pass_record.record_mdate == self.pass_record.pass_mdate
        else:
            assert self.pass_record.record_mdate != self.pass_record.pass_mdate

    def test_set_username(self):
        tests = ["a1b2c3", "t3stt3stt3st"]
        for username in tests:
            self.pass_record.set_username(username)
            self.pass_record.set_mdate(self.time_oracle.get_current_time())
            self.test_get_mdate(pass_mdate=False)
            assert self.pass_record.username == username

    def test_set_password(self):
        tests = ["admin123", "!)@&4c!&*!G(nD$"]
        for password in tests:
            self.pass_record.set_password(password)
            self.pass_record.set_mdate(self.time_oracle.get_current_time())
            self.pass_record.set_pass_mdate(self.pass_record.record_mdate)
            self.test_get_mdate(pass_mdate=True)
            assert self.pass_record.password == password

    def test_set_tag(self):
        tests = ["social1", "financial"]
        for tag in tests:
            self.pass_record.set_tag(tag)
            self.pass_record.set_mdate(self.time_oracle.get_current_time())
            self.test_get_mdate(pass_mdate=False)
            assert self.pass_record.tag == tag

    def test_set_url(self):
        tests = ["www.a1b2c3.net", "t3stt3stt3st"]
        for url in tests:
            self.pass_record.set_url(url)
            self.pass_record.set_mdate(self.time_oracle.get_current_time())
            self.test_get_mdate(pass_mdate=False)
            assert self.pass_record.url == url

    def test_set_notes(self):
        tests = [
            "Proin bibendum libero quam, ullamcorper luctus magna viverra nec. Mauris bibendum ex quam. Fusce non",
            "Cras ullamcorper cursus tincidunt. Curabitur a cursus quam, at egestas nisi. Nam dignissim, libero at",
        ]
        for notes in tests:
            self.pass_record.set_notes(notes)
            self.pass_record.set_mdate(self.time_oracle.get_current_time())
            self.test_get_mdate(pass_mdate=False)
            assert self.pass_record.notes == notes

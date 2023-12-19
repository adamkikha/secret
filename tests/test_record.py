import pytest
from src.model.record import Record
import time


class Test_Record:
    record = Record(
        1,
        "abcd",
        "1234",
        "work",
        "www.website.com",
        "the quick brown fox jumps over the lazy dog",
    )

    def test_get_mdate(self, pass_mdate: bool = False):
        assert 0 <= time.time() - self.record.get_mdate(False) <= 2
        if pass_mdate:
            assert self.record.get_mdate(False) == self.record.get_mdate(True)

    def test_set_username(self):
        tests = ["a1b2c3", "t3stt3stt3st"]
        for username in tests:
            self.record.set_username(username)
            self.test_get_mdate()
            assert self.record.username == username

    def test_set_password(self):
        tests = ["admin123", "!)@&4c!&*!G(nD$"]
        for password in tests:
            self.record.set_password(password)
            self.test_get_mdate(True)
            assert self.record.password == password

    def test_set_tag(self):
        tests = ["social1", "financial"]
        for tag in tests:
            self.record.set_tag(tag)
            self.test_get_mdate()
            assert self.record.tag == tag

    def test_set_url(self):
        tests = ["www.a1b2c3.net", "t3stt3stt3st"]
        for url in tests:
            self.record.set_url(url)
            self.test_get_mdate()
            assert self.record.url == url

    def test_set_notes(self):
        tests = [
            "Proin bibendum libero quam, ullamcorper luctus magna viverra nec. Mauris bibendum ex quam. Fusce non",
            "Cras ullamcorper cursus tincidunt. Curabitur a cursus quam, at egestas nisi. Nam dignissim, libero at",
        ]
        for notes in tests:
            self.record.set_notes(notes)
            self.test_get_mdate()
            assert self.record.notes == notes

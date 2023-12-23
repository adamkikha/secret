import pytest
from src.model.file_record import FileRecord
from src.utils import TimeOracle


class Test_FileRecord:
    time_oracle = TimeOracle()
    file_record = FileRecord(
        0,
        "abcd",
        1234,
        "work",
        "the quick brown fox jumps over the lazy dog",
        time_oracle.get_current_time(),
    )

    def test_set_name(self):
        tests = ["a1b2c3", "t3stt3stt3st"]
        for name in tests:
            self.file_record.set_name(name)
            self.file_record.set_mdate(self.time_oracle.get_current_time())
            assert (
                0
                <= self.time_oracle.get_current_time() - self.file_record.record_mdate
                <= 2
            )
            assert self.file_record.name == name

    def test_set_tag(self):
        tests = ["social1", "financial"]
        for tag in tests:
            self.file_record.set_tag(tag)
            self.file_record.set_mdate(self.time_oracle.get_current_time())
            assert (
                0
                <= self.time_oracle.get_current_time() - self.file_record.record_mdate
                <= 2
            )
            assert self.file_record.tag == tag

    def test_set_size(self):
        tests = [0, 999999999]
        for size in tests:
            self.file_record.set_size(size)
            self.file_record.set_mdate(self.time_oracle.get_current_time())
            assert (
                0
                <= self.time_oracle.get_current_time() - self.file_record.record_mdate
                <= 2
            )
            assert self.file_record.size == size

    def test_set_notes(self):
        tests = [
            "Proin bibendum libero quam, ullamcorper luctus magna viverra nec. Mauris bibendum ex quam. Fusce non",
            "Cras ullamcorper cursus tincidunt. Curabitur a cursus quam, at egestas nisi. Nam dignissim, libero at",
        ]
        for notes in tests:
            self.file_record.set_notes(notes)
            self.file_record.set_mdate(self.time_oracle.get_current_time())
            assert (
                0
                <= self.time_oracle.get_current_time() - self.file_record.record_mdate
                <= 2
            )
            assert self.file_record.notes == notes

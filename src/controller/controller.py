import os
from src.controller.crypto import kdf, encrypt, decrypt
from math import log2


class Controller:
    def __init__(self):
        self.model = None
        self.file_path = None

    def create_file(self, master_key, file_path):
        self.file_path = file_path
        self.model.initialize(file_path, create=True)
        self.salt = os.urandom(16)
        self.derived_key = kdf(master_key, self.salt)
        self.nonce = os.urandom(24)
        aad = self.nonce + self.salt  # concatenate nonce and salt
        self.ciphertext, self.tag = encrypt(
            self.model.serialize_records(), self.derived_key, self.nonce, aad=aad
        )
        self.model.save_file(self.ciphertext, self.tag, self.nonce, self.salt)

    def open_file(self, master_key, file_path):
        self.file_path = file_path
        try:
            self.model.initialize(file_path, create=False)
        except Exception as e:
            self.file_path = None
            print(f"Opening file failed: {e}")
            return False
        self.salt = self.model.salt
        self.derived_key = kdf(master_key, self.salt)
        self.nonce = self.model.nonce
        self.ciphertext = self.model.ciphertext
        self.tag = self.model.tag
        aad = self.nonce + self.salt  # concatenate nonce and salt
        try:
            self.plaintext = decrypt(
                self.ciphertext, self.tag, self.derived_key, self.nonce, aad
            )
        except Exception as e:
            self.file_path = None
            print(f"Decryption failed: {e}")
            return False
        self.model.construct_records(self.plaintext)
        self.plaintext = None
        return True

    def save_file(self):
        if self.file_path:
            self.nonce = os.urandom(24)
            aad = self.nonce + self.salt
            self.ciphertext, self.tag = encrypt(
                self.model.serialize_records(), self.derived_key, self.nonce, aad=aad
            )
            self.model.save_file(self.ciphertext, self.tag, self.nonce, self.salt)
            return True
        else:
            return False

    def close_file(self, save: bool):
        if save:
            self.save_file()
        self.derived_key = None
        self.file_path = None
        self.model.close_file()

    def delete_record(self, id: int):
        return self.model.delete_record(id) == True

    def filter_search(self, filter_list: list[str], search_term: str):
        self.model.filter_search(filter_list, search_term)

    @staticmethod
    def get_password_entropy(password: str):
        char_set_len = len(set(password))
        pass_len = len(password)
        if char_set_len:
            return pass_len * log2(char_set_len)
        return 0

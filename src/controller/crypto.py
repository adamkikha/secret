from argon2 import Type
from argon2.low_level import hash_secret_raw
from Cryptodome.Cipher import ChaCha20_Poly1305


def kdf(password, salt):
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )


def encrypt(plaintext, key, nonce, aad=b""):
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)
    ciphertext = cipher.encrypt(plaintext)
    tag = cipher.digest()
    return ciphertext, tag


def decrypt(ciphertext, tag, key, nonce, aad=b""):
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

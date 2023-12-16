from argon2 import Type
from argon2.low_level import hash_secret_raw


def kdf(password, salt):
    return hash_secret_raw(
        secret=password.encode(),
        salt=salt.encode(),
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )

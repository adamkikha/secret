import binascii
from src.controller.crypto import kdf


def test_kdf():
    # [(password, salt, expected_hash_hex),..]
    tests = [
        (
            "c0rRec! h_rse Ba340#",
            "LX05GphLi7BloIE5",
            "2500600597f27c8901212f8b446c8996790c079ec63bcdf79807bb565d6cc007",
        ),
        (
            "2se048",
            "wh2J#_k xSeJA!nO",
            "7456418d68b29f0709b6f2ac8e102486b8d8ea74fa7c86fc4f63f81acca2dcf3",
        ),
        (
            "2se049",
            "wh2J#_k xSeJA!nO",
            "009b583b110029bd2eba6099f8493acab6671a2b082b99251b7331f7aea6ac9a",
        ),
        (
            "2se049",
            "wh2J#_k xSeJA!nP",
            "b6a5dbe169d6bfd8edda5fe9623dff7d30aeb3d80e8d36f738fdb00d3ac0cba3",
        ),
        (
            "nx3gfai8/VUlI6?R7:}Zi%27_OUqp) &I}bV;sJa",
            "578O[]qdyEv/yQ?`",
            "cbef33fd4aac018d73efcfdf494ede48e13d7d07e84ef39e8378338b143399a3",
        ),
    ]
    for password, salt, expected_hash_hex in tests:
        expected_hash = binascii.unhexlify(expected_hash_hex)
        computed_hash = kdf(password, salt)
        assert computed_hash == expected_hash

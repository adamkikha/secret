import pytest
import random
import binascii
from src.controller.crypto import kdf
from src.controller.crypto import encrypt, decrypt


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
        computed_hash = kdf(password, salt.encode())
        assert computed_hash == expected_hash


def induce_error(component):
    byte_list = list(component)
    byte_index = random.randrange(len(byte_list))
    bit_index = random.randrange(8)
    byte_list[byte_index] ^= 1 << bit_index
    return bytes(byte_list)


def test_encrypt():
    # [(plaintext_hex, key_hex, nonce_hex, aad_hex, expected_ciphertext_hex, expected_tag_hex)]
    tests = [
        (
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555657",
            "50515253c0c1c2c3c4c5c6c7",
            "bd6d179d3e83d43b9576579493c0e939572a1700252bfaccbed2902c21396cbb731c7f1b0b4aa6440bf3a82f4eda7e39ae64c6708c54c216cb96b72e1213b4522f8c9ba40db5d945b11b69b982c1bb9e3f3fac2bc369488f76b2383565d3fff921f9664c97637da9768812f615c68b13b52e",
            "c0875924c1c7987947deafd8780acf49",
        ),
        (
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555658",
            "50515253c0c1c2c3c4c5c6c7",
            "65032f227e672aaf3d102e073e4f1c386abab35ee19a50deb91a4ae3aeb7c687bf89e39fc459675deb350c69bb5b7b372bea9b0561a5046c7aeedcd2456faa4a301a137209d61da415499a44cbf6d867e019831b89bea709a3a706026c910c523f814911e77b826af350a9fd2a93097fa84b",
            "7ea2404b69a2a6182be9992ce53701bf",
        ),
    ]

    for (
        plaintext_hex,
        key_hex,
        nonce_hex,
        aad_hex,
        expected_ciphertext_hex,
        expected_tag_hex,
    ) in tests:
        plaintext = binascii.unhexlify(plaintext_hex)
        key = binascii.unhexlify(key_hex)
        nonce = binascii.unhexlify(nonce_hex)
        aad = binascii.unhexlify(aad_hex)
        expected_ciphertext = binascii.unhexlify(expected_ciphertext_hex)
        expected_tag = binascii.unhexlify(expected_tag_hex)
        computed_ciphertext, computed_tag = encrypt(plaintext, key, nonce, aad)
        assert computed_ciphertext == expected_ciphertext
        assert computed_tag == expected_tag


def test_decrypt():
    # [(ciphertext_hex, tag_hex, key_hex, nonce_hex, aad_hex, expected_plaintext_hex)]
    tests = [
        (
            "bd6d179d3e83d43b9576579493c0e939572a1700252bfaccbed2902c21396cbb731c7f1b0b4aa6440bf3a82f4eda7e39ae64c6708c54c216cb96b72e1213b4522f8c9ba40db5d945b11b69b982c1bb9e3f3fac2bc369488f76b2383565d3fff921f9664c97637da9768812f615c68b13b52e",
            "c0875924c1c7987947deafd8780acf49",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555657",
            "50515253c0c1c2c3c4c5c6c7",
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
        ),
        (
            "65032f227e672aaf3d102e073e4f1c386abab35ee19a50deb91a4ae3aeb7c687bf89e39fc459675deb350c69bb5b7b372bea9b0561a5046c7aeedcd2456faa4a301a137209d61da415499a44cbf6d867e019831b89bea709a3a706026c910c523f814911e77b826af350a9fd2a93097fa84b",
            "7ea2404b69a2a6182be9992ce53701bf",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555658",
            "50515253c0c1c2c3c4c5c6c7",
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
        ),
    ]

    random.seed(42)

    for (
        ciphertext_hex,
        tag_hex,
        key_hex,
        nonce_hex,
        aad_hex,
        expected_plaintext_hex,
    ) in tests:
        ciphertext = binascii.unhexlify(ciphertext_hex)
        tag = binascii.unhexlify(tag_hex)
        key = binascii.unhexlify(key_hex)
        nonce = binascii.unhexlify(nonce_hex)
        aad = binascii.unhexlify(aad_hex)
        expected_plaintext = binascii.unhexlify(expected_plaintext_hex)

        # Incorrect ciphertext
        incorrect_ciphertext = induce_error(ciphertext)
        with pytest.raises(ValueError):
            decrypt(incorrect_ciphertext, tag, key, nonce, aad)
        # Incorrect tag
        incorrect_tag = induce_error(tag)
        with pytest.raises(ValueError):
            decrypt(ciphertext, incorrect_tag, key, nonce, aad)
        # Incorrect key
        incorrect_key = induce_error(key)
        with pytest.raises(ValueError):
            decrypt(ciphertext, tag, incorrect_key, nonce, aad)
        # Incorrect nonce
        incorrect_nonce = induce_error(nonce)
        with pytest.raises(ValueError):
            decrypt(ciphertext, tag, key, incorrect_nonce, aad)
        if aad:  # May be empty
            # Incorrect aad
            incorrect_aad = induce_error(aad)
            with pytest.raises(ValueError):
                decrypt(ciphertext, tag, key, nonce, incorrect_aad)

        computed_plaintext = decrypt(ciphertext, tag, key, nonce, aad)
        assert computed_plaintext == expected_plaintext


def test_encrypt_decrypt():
    # [(plaintext_hex, key_hex, nonce_hex, aad_hex)]
    tests = [
        (
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555657",
            "50515253c0c1c2c3c4c5c6c7",
        ),
        (
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555658",
            "50515253c0c1c2c3c4c5c6c7",
        ),
        (
            "4c616469657320616e642047656e746c656d656e206f662074686520636c617373206f66202739393a204966204920636f756c64206f6666657220796f75206f6e6c79206f6e652074697020666f7220746865206675747572652c2073756e73637265656e20776f756c642062652069742e",
            "808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f",
            "404142434445464748494a4b4c4d4e4f5051525354555658",
            "",
        ),
    ]

    # seed random test generation
    random.seed(42)

    for _ in range(1000):
        # Generate random data
        plaintext = bytes(random.getrandbits(8) for _ in range(random.randint(1, 1024)))
        key = bytes(random.getrandbits(8) for _ in range(32))
        nonce = bytes(random.getrandbits(8) for _ in range(24))
        aad = bytes(random.getrandbits(8) for _ in range(random.randint(0, 256)))

        # Convert to hex
        plaintext_hex = binascii.hexlify(plaintext).decode()
        key_hex = binascii.hexlify(key).decode()
        nonce_hex = binascii.hexlify(nonce).decode()
        aad_hex = binascii.hexlify(aad).decode()

        # Add to tests
        tests.append((plaintext_hex, key_hex, nonce_hex, aad_hex))

    for (
        plaintext_hex,
        key_hex,
        nonce_hex,
        aad_hex,
    ) in tests:
        plaintext = binascii.unhexlify(plaintext_hex)
        key = binascii.unhexlify(key_hex)
        nonce = binascii.unhexlify(nonce_hex)
        aad = binascii.unhexlify(aad_hex)
        computed_ciphertext, computed_tag = encrypt(plaintext, key, nonce, aad)

        # Incorrect ciphertext
        incorrect_ciphertext = induce_error(computed_ciphertext)
        with pytest.raises(ValueError):
            decrypt(incorrect_ciphertext, computed_tag, key, nonce, aad)
        # Incorrect tag
        incorrect_tag = induce_error(computed_tag)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, incorrect_tag, key, nonce, aad)
        # Incorrect key
        incorrect_key = induce_error(key)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, computed_tag, incorrect_key, nonce, aad)
        # Incorrect nonce
        incorrect_nonce = induce_error(nonce)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, computed_tag, key, incorrect_nonce, aad)
        if aad:  # May be empty
            # Incorrect aad
            incorrect_aad = induce_error(aad)
            with pytest.raises(ValueError):
                decrypt(computed_ciphertext, computed_tag, key, nonce, incorrect_aad)

        computed_plaintext = decrypt(computed_ciphertext, computed_tag, key, nonce, aad)
        assert plaintext == computed_plaintext

    # Without aad
    for (
        plaintext_hex,
        key_hex,
        nonce_hex,
        aad_hex,
    ) in tests:
        plaintext = binascii.unhexlify(plaintext_hex)
        key = binascii.unhexlify(key_hex)
        nonce = binascii.unhexlify(nonce_hex)
        computed_ciphertext, computed_tag = encrypt(plaintext, key, nonce)

        # Incorrect ciphertext
        incorrect_ciphertext = induce_error(computed_ciphertext)
        with pytest.raises(ValueError):
            decrypt(incorrect_ciphertext, computed_tag, key, nonce)
        # Incorrect tag
        incorrect_tag = induce_error(computed_tag)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, incorrect_tag, key, nonce)
        # Incorrect key
        incorrect_key = induce_error(key)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, computed_tag, incorrect_key, nonce)
        # Incorrect nonce
        incorrect_nonce = induce_error(nonce)
        with pytest.raises(ValueError):
            decrypt(computed_ciphertext, computed_tag, key, incorrect_nonce)

        computed_plaintext = decrypt(computed_ciphertext, computed_tag, key, nonce)
        assert plaintext == computed_plaintext

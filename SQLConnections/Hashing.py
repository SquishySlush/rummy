import os


def simple_hash(input_str, salt):
    """
    Generate a custom hash value from an input string and salt.

    The function combines the input text with the salt, then repeatedly
    applies bitwise and arithmetic operations to produce a fixed hash value.

    Args:
        input_str (str): The string to hash.
        salt (str): The salt added to the input before hashing.

    Returns:
        int: The resulting hash value as an integer.
    """
    hash_vector = 2166136261

    combined = input_str + salt

    for char in combined:
        # Mix each character into the hash using XOR and bit shifting.
        hash_vector ^= ord(char)
        hash_vector *= 53383619654664048229
        hash_vector &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        hash_vector ^= (hash_vector >> 13)
        hash_vector ^= (hash_vector << 7) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    return hash_vector


def hash_password(password, salt=None):
    """
    Hash a password using a salt.

    If a salt is supplied, it is reused so the same password can be checked
    against a stored hash. If no salt is supplied, a new random salt is created.

    The password is hashed repeatedly to make the final value harder to reverse.

    Args:
        password (str): The password to hash.
        salt (str, optional): An existing salt. If omitted, a new salt is generated.

    Returns:
        tuple: The salt used and the final hash as a hexadecimal string.
    """
    if salt is not None:
        hash_value = simple_hash(password, salt)
    else:
        salt = os.urandom(8).hex()
        hash_value = simple_hash(password, salt)

    # Repeat the hashing process multiple times to increase security.
    for _ in range(1000):
        hash_value = simple_hash(str(hash_value), salt)

    return salt, format(hash_value, "032x")
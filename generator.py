import secrets
import string


def generate_password(length):
    length = int(length)
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password
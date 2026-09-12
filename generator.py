import secrets
import string


def generate_password(
    length: int,
    use_letters: bool=True,
    use_digits: bool=True,
    use_symbols: bool=True
) -> str:
    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_symbols:
        #characters += string.punctuation
        characters += "!@#$%^&*()-_=+"

    if not characters:
        raise ValueError("At least one character type must be selected.")
    # length = int(length)
    # characters = string.ascii_letters + string.digits + string.punctuation
    #
    # password = ''.join(secrets.choice(characters) for _ in range(length))

    return ''.join(secrets.choice(characters) for _ in range(length))
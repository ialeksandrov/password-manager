import os
import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken


def derive_key(master_password: str, salt: bytes) -> bytes:
    key = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode(),
        salt,
        iterations=390_000,
    )
    return base64.urlsafe_b64encode(key)


def init_master(conn, master_password: str) -> Fernet:
    salt = os.urandom(32)
    key = derive_key(master_password, salt)
    f = Fernet(key)
    verify_token = f.encrypt(b"__VAULT_OK__")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO master (salt, verify) VALUES (?, ?)", (salt, verify_token))
    conn.commit()
    cursor.close()
    return f


def unlock_vault(conn, master_password: str) -> Fernet:
    cursor = conn.cursor()
    cursor.execute("SELECT salt, verify FROM master")
    row = cursor.fetchone()
    cursor.close()
    if not row:
        raise RuntimeError("Vault not initialized.")
    salt, verify_token = row
    key = derive_key(master_password, salt)
    f = Fernet(key)
    try:
        result = f.decrypt(verify_token)
        if result != b"__VAULT_OK__":
            raise ValueError
    except (InvalidToken, ValueError):
        raise RuntimeError("Wrong master password.")
    return f
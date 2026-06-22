import sqlite3
from cryptography.fernet import Fernet


DB_FILE = 'password_manager.db'

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        title TEXT,
        username TEXT,
        password TEXT,
        UNIQUE(title, username)
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS master (
        id      INTEGER PRIMARY KEY,
        salt    BLOB NOT NULL,
        verify  BLOB NOT NULL
    )
''')
conn.commit()
conn.commit()
cursor.close()


def create_password(fernet: Fernet, title, username, password):
    enc_password = fernet.encrypt(password.encode())
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (title, username, password) VALUES (?, ?, ?)', (title, username, enc_password))

    conn.commit()
    cursor.close()


def update_password(fernet: Fernet, title, username, new_password):
    enc_password = fernet.encrypt(new_password.encode())
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET password = ? WHERE title = ? AND username = ?', (enc_password, title, username))

    conn.commit()
    cursor.close()


def get_password(fernet: Fernet, username):
    cursor = conn.cursor()
    if username:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()

    return [
        (id_, title, uname, fernet.decrypt(enc_password).decode())
        for id_, title, uname, enc_password in users
    ]

def delete_password(title):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE title = ?', (title,))
    conn.commit()
    cursor.close()
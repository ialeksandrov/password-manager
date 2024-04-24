import sys
import random
import string
import argparse
import sqlite3


conn = sqlite3.connect('password_manager.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        title TEXT,
        username TEXT,
        password TEXT
    )
''')

conn.commit()
cursor.close()


def generate_password(length):
    length = int(args.length)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    numbers = string.digits
    symbols = string.punctuation
    full_set = lower + upper + numbers + symbols
    temp = random.sample(full_set, length)
    password = "".join(temp)

    return password


def create_password(title, username, password):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (title, username, password) VALUES (?, ?, ?)', (title, username, password))
    conn.commit()
    cursor.close()

    return title, username, password


def update_password(title, username, new_password):
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = ? WHERE username = ? and title = ?', (new_password, username, title))
    conn.commit()
    cursor.close()



def get_password(username):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    cursor.close()

    return user


def delete_password(username):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    conn.commit()
    cursor.close()



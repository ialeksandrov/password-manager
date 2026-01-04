#!/usr/bin/python3

import random
import string
import argparse
import sqlite3


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

conn.commit()
cursor.close()


def generate_password(length):
    length = int(args.length)
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    return password


def create_password(title, username, password):
    cursor = conn.cursor()

    cursor.execute('INSERT INTO users (title, username, password) VALUES (?, ?, ?)', (title, username, password))

    conn.commit()
    cursor.close()


def update_password(title, username, new_password):
    cursor = conn.cursor()

    cursor.execute('UPDATE users SET password = ? WHERE title = ? AND username = ?', (new_password, title, username))

    conn.commit()
    cursor.close()


def get_password(username):
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    cursor.close()

    return user

def delete_password(title):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE title = ?', (title,))
    conn.commit()
    cursor.close()


parser = argparse.ArgumentParser(prog='Password Manager', description='Managing passwords and users')

parser.add_argument('action', choices=['add', 'list', 'generate', 'update', 'delete'], help='Actions to perform')
parser.add_argument('--title', help='Title of the password entry')
parser.add_argument('--username', help='Username for the password entry')
parser.add_argument('--password', help='Password for the entry')
parser.add_argument('--length', help='Length of the password entry')

args = parser.parse_args()

if args.action == 'add':
    create_password(args.title, args.username, args.password)
elif args.action == 'update':
    update_password(args.title, args.username, args.password)
elif args.action == 'list':
    print(get_password(args.username))
elif args.action == 'generate':
    print(generate_password(args.length))
elif args.action == 'delete':
    delete_password(args.title)


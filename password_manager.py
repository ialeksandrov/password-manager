#!/usr/bin/python3

import os
import argparse
import sqlite3
import getpass

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

if __name__ == "__main__":
    import getpass
    parser = argparse.ArgumentParser(prog='Password Manager', description='Managing passwords and users')

    parser.add_argument('action', choices=['add', 'list', 'generate', 'update', 'delete'], help='Actions to perform')
    parser.add_argument('--title', help='Title of the password entry')
    parser.add_argument('--username', help='Username for the password entry')
    parser.add_argument('--length', help='Length of the password entry')

    args = parser.parse_args()

    # --- vault setup or unlock
    vault_exists = conn.execute("SELECT COUNT(*) FROM master").fetchone()[0] > 0

    if not vault_exists:
        print("First run — set your master password.")
        master = getpass.getpass("Master password: ")
        confirm = getpass.getpass("Confirm: ")
        if master != confirm:
            print("Passwords don't match.")
            exit(1)
        fernet = init_master(master)
        print("Vault created successfully.")
    else:
        master = getpass.getpass("Master password: ")
        try:
            fernet = unlock_vault(master)
        except RuntimeError as e:
            print(f"Error: {e}")
            exit(1)

    # --- actions
    if args.action == 'add':
        password = getpass.getpass("Password to store: ")
        create_password(fernet, args.title, args.username, password)
        print(f"Entry '{args.title}' added successfully.")
    elif args.action == 'update':
        password = getpass.getpass("New password: ")
        update_password(fernet, args.title, args.username, password)
        print(f"Entry '{args.title}' updated successfully.")
    elif args.action == 'list':
        entries = get_password(fernet, args.username)
        if not entries:
            print("No entries found.")
        else:
            for id_, title, uname, password in entries:
                print(f"Title: {title} | Username: {uname} | Password: {password}")
    elif args.action == 'generate':
        print(generate_password(args.length))
    elif args.action == 'delete':
        delete_password(args.title)
        print(f"Entry '{args.title}' deleted successfully.")


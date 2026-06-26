#!/usr/bin/python3

import argparse
import sqlite3
import getpass

from db import get_conn, setup_db, create_password, get_password, update_password, delete_password
from crypto_utils import init_master, unlock_vault
from generator import generate_password


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Password Manager', description='Managing passwords and users')

    parser.add_argument('action', choices=['add', 'list', 'generate', 'update', 'delete'], help='Actions to perform')
    parser.add_argument('--title', help='Title of the password entry')
    parser.add_argument('--username', help='Username for the password entry')
    parser.add_argument('--length', help='Length of the password entry')

    args = parser.parse_args()

    conn = get_conn()
    setup_db(conn)

    # --- vault setup or unlock
    vault_exists = conn.execute("SELECT COUNT(*) FROM master").fetchone()[0] > 0

    if not vault_exists:
        print("First run — set your master password.")
        master = getpass.getpass("Master password: ")
        confirm = getpass.getpass("Confirm: ")
        if master != confirm:
            print("Passwords don't match.")
            exit(1)
        fernet = init_master(conn, master)
        print("Vault created successfully.")
    else:
        master = getpass.getpass("Master password: ")
        try:
            fernet = unlock_vault(conn, master)
        except RuntimeError as e:
            print(f"Error: {e}")
            exit(1)

    # --- actions
    if args.action == 'add':
        if not args.title or not args.username:
            print("Error: --title and --username are required for add.")
            exit(1)
        password = getpass.getpass("Password to store: ")
        create_password(conn, fernet, args.title, args.username, password)
        print(f"Entry '{args.title}' added successfully.")
    elif args.action == 'update':
        if not args.title or not args.username:
            print("Error: --title and --username are required for update.")
            exit(1)
        password = getpass.getpass("New password: ")
        update_password(conn, fernet, args.title, args.username, password)
        print(f"Entry '{args.title}' updated successfully.")
    elif args.action == 'list':
        entries = get_password(conn, fernet, args.username)
        if not entries:
            print("No entries found.")
        else:
            for id_, title, uname, password in entries:
                print(f"Title: {title} | Username: {uname} | Password: {password}")
    elif args.action == 'generate':
        print(generate_password(args.length))
    elif args.action == 'delete':
        if not args.title:
            print("Error: --title is required for delete.")
            exit(1)
        delete_password(conn, args.title)
        print(f"Entry '{args.title}' deleted successfully.")

    conn.close()
import random
import string
import argparse
import sqlite3

from passlib.hash import argon2


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
    
    hashed_password = argon2.hash(password)
    
    try:
        cursor.execute('INSERT INTO users (title, username, password) VALUES (?, ?, ?)', (title, username, hashed_password))
        print(f'Password added: Title={title}, Username={username}')
    except sqlite3.IntegrityError:
        print(f'Entry with Title={title} and Username={username} already exists.')

    conn.commit()
    cursor.close()


def update_password(title, username, new_password):
    cursor = conn.cursor()

    hashed_password = argon2.hash(new_password)

    cursor.execute('UPDATE users SET password = ? WHERE title = ? AND username = ?', (hashed_password, title, username))
    if cursor.rowcount == 0:
        print("No entry found with the given title and username")
    else:
        print("Password updated successfully")

    conn.commit()
    cursor.close()


def verify_password(title, username, password):
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM users WHERE title = ? AND username = ?', (title, username))

    result = cursor.fetchone()

    if result:
        hashed_password = result[0]

        if argon2.verify(password, hashed_password):
            print("Password is correct")
        else:
            print("Password is incorrect")
    else:
        print("No entry found with the given title and username")

    cursor.close()


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
elif args.action == 'verify':
    print(verify_password(args.title, args.username, args.password))
elif args.action == 'generate':
    print(generate_password(args.length))
elif args.action == 'delete':
    delete_password(args.title)


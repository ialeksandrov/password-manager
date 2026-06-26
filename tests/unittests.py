import unittest
import sqlite3
import base64
import hashlib
import os
import sys

from cryptography import fernet

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.fernet import Fernet
from generator import generate_password
from crypto_utils import derive_key, init_master, unlock_vault
from db import create_password, get_password, update_password, delete_password


class TestPasswordManager(unittest.TestCase):
    def setUp(self):
        """Runs before every test - creates a fresh in-memory DB and Fernet."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                title TEXT,
                username TEXT,
                password TEXT,
                UNIQUE(title, username)
            )
        ''')
        self.conn.execute('''
                CREATE TABLE IF NOT EXISTS master (
                    id      INTEGER PRIMARY KEY,
                    salt    BLOB NOT NULL,
                    verify  BLOB NOT NULL
                )
            ''')
        self.conn.commit()
        salt = os.urandom(32)
        key = derive_key("testmaster", salt)
        self.fernet = Fernet(key)

    def tearDown(self):
        """Runs after every test - coses the DB connection."""
        self.conn.close()
    def test_remove_duplicate_password(self):
        create_password(self.conn, self.fernet, "github", "test", "secret123456")
        with self.assertRaises(Exception):
            create_password(self.conn, self.fernet, "github", "test", "secret1236")

    def test_remove_password(self):
        create_password(self.conn, self.fernet, "github", "test", "secret123456")
        delete_password(self.conn, "github")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 0)

    def test_generate_password(self):
        password = generate_password(12)
        self.assertEqual(len(password), 12)

    def test_generate_password_with_custom_length(self):
        password = generate_password(20)
        self.assertEqual(len(password), 20)

    def test_save_password(self):
        create_password(self.conn, self.fernet, "github", "test", "secret123456")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][1], "github")
        self.assertEqual(entries[0][2], "test")
        self.assertEqual(entries[0][3], "secret123456")

    def test_list_all_saved_passwords(self):
        create_password(self.conn, self.fernet, "github", "test", "secret123")
        create_password(self.conn, self.fernet, "gitlab", "test", "secret1234")
        create_password(self.conn, self.fernet, "bitbucket", "test", "secret12345")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 3)


    def test_display_last_inserted_password(self):
        create_password(self.conn, self.fernet, "github", "test", "secret123")
        create_password(self.conn, self.fernet, "gitlab", "test", "secret1234")
        create_password(self.conn, self.fernet, "bitbucket", "test", "secret12345")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(entries[-1][3], "secret12345")


    def test_add_custom_password(self):
        create_password(self.conn, self.fernet, "abv", "ialeksandrov", "Firestarter23")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(entries[0][3], "Firestarter23")


    def test_wrong_master_password(self):
        init_master(self.conn, "testmaster")
        with self.assertRaises(Exception):
            unlock_vault(self.conn, "testmasterrrr")


    def test_correct_master_password(self):
        init_master(self.conn, "testmaster")
        fernet = unlock_vault(self.conn, "testmaster")
        self.assertIsInstance(fernet, Fernet)


    def test_add_password_without_username(self):
        with self.assertRaises(Exception):
            create_password(self.conn, self.fernet, "github", None, "secret123")


    def test_password_is_encrypted_in_db(self):
        create_password(self.conn, self.fernet, "github", "johny_depp", "secret123")
        raw = self.conn.execute("SELECT password FROM users;").fetchone()[0]
        self.assertNotEqual(raw, "secret123")


    def test_list_empty_db(self):
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 0)


    def test_list_nonexistent_username(self):
        create_password(self.conn, self.fernet, "github", "test5432", "secret123")
        entries = get_password(self.conn, self.fernet, "Nonexistent")
        self.assertEqual(len(entries), 0)


    def test_update_nonexistent_entry(self):
        update_password(self.conn, self.fernet, "Nonexistent", "secret123", "secret1234")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 0)


    def test_delete_nonexistent_entry(self):
        delete_password(self.conn, "Nonexistent")
        entries = get_password(self.conn, self.fernet, None)
        self.assertEqual(len(entries), 0)


if __name__ == "__main__":
    unittest.main()

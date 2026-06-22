import unittest
import sqlite3
import base64
import hashlib
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptography.fernet import Fernet
from password_manager import derive_key, create_password, get_password, update_password, delete_password
from generator import generate_password

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
        self.conn.commit()
        salt = os.urandom(32)
        key = derive_key("testmaster", salt)
        self.fernet = Fernet(key)

    def tearDown(self):
        """Runs after every test - coses the DB connection."""
        self.conn.close()
    def test_remove_duplicate_password(self):
        pass

    def test_remove_password(self):
        pass

    def test_generate_password(self):
        password = generate_password(12)
        self.assertEqual(len(password), 12)

    def test_generate_password_with_custom_length(self):
        password = generate_password(20)
        self.assertEqual(len(password), 20)

    def test_save_password(self):
        pass

    def test_list_all_saved_passwords(self):
        pass

    def test_display_last_saved_password(self):
        pass

    def test_add_custom_password(self):
        pass


if __name__ == "__main__":
    unittest.main()

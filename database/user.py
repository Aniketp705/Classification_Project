import sqlite3
import hashlib
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'user_credentials.db')


def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user_table():
    """Creates the users table if it doesn't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes a password using SHA256."""
    # In a real application, use a unique salt per user and a stronger hashing algorithm like Argon2 or scrypt
    salt = "your_secret_salt" # This should be a securely generated and stored salt
    salted_password = salt.encode('utf-8') + password.encode('utf-8')
    hashed_password = hashlib.sha256(salted_password).hexdigest()
    return hashed_password

def add_user(username, password):
    """Adds a new user to the database.

    Args:
        username (str): The username for the new user.
        password (str): The plain text password for the new user.

    Returns:
        bool: True if user was added successfully, False otherwise (e.g., username exists).
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    password_h = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                       (username, password_h))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Handles cases where username already exists
        print(f"Username '{username}' already exists.")
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verifies a user's credentials.

    Args:
        username (str): The username to verify.
        password (str): The plain text password to verify.

    Returns:
        bool: True if credentials are valid, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user_record = cursor.fetchone()
    conn.close()

    if user_record:
        stored_password_hash = user_record['password_hash']
        input_password_hash = hash_password(password)
        return stored_password_hash == input_password_hash
    return False
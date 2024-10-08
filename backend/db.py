import sqlite3

ACCOUNTS_DB = "accounts.db"


class AccountType:
    ADMIN = "ADMIN"
    PATIENT = "PATIENT"
    MONITOR = "MONITOR"


def create_table():
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                account_type TEXT
            )
            """
        )
        conn.commit()


def add_account(username: str, password: str, account_type: str):
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO accounts (username, password, account_type) VALUES (?, ?, ?)",
                (username, password, account_type),
            )
            conn.commit()
            print("Account created successfully.")
            return None
        except sqlite3.IntegrityError:
            print("Account already exists")
            return "Account already exists"


def delete_account(username: str):
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM accounts WHERE username = ?", (username,)
            )
            conn.commit()
            print("Account deleted successfully.")
            return None
        except sqlite3.IntegrityError:
            print("Account does not exist.")
            return "Account does not exist"


def authenticate(username: str, password: str) -> str:
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username,),
        )
        account = cursor.fetchone()
        if not account:
            print("Nonexistent account.")
            return "Nonexistent account"

        cursor.execute(
            "SELECT * FROM accounts WHERE username = ? AND password = ?",
            (username, password),
        )
        account = cursor.fetchone()
        if account:
            print("Authentication successful.")
            return "Authentication successful"
        else:
            print("Incorrect password.")
            return "Incorrect password"


def change_account_password(username: str, password: str):
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE accounts SET password = ? WHERE username = ?",
            (password, username),
        )


def get_account_type(username: str) -> str | None:
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT account_type FROM accounts WHERE username = ?",
            (username,),
        )
        account_type = cursor.fetchone()
        if account_type is None:
            return None
        else:
            return account_type[0]


def get_all_accounts():
    with sqlite3.connect(ACCOUNTS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()
        return accounts


create_table()

import sqlite3

conn = sqlite3.connect(
    "cognit.db",
    check_same_thread=False
)

cursor = conn.cursor()

# USERS

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT,
    premium INTEGER DEFAULT 0
)
""")

# SETTINGS

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    memory INTEGER DEFAULT 0,
    consent INTEGER DEFAULT 0
)
""")

# CHAT HISTORY

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    role TEXT,
    message TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# LIBRARY

cursor.execute("""
CREATE TABLE IF NOT EXISTS library(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    description TEXT,
    price REAL,
    rent_price REAL,
    file_path TEXT
)
""")
# (sample insert handled below only if table empty)
# Ensure required columns exist on older DBs where table was created without them
cursor.execute("PRAGMA table_info(library)")
existing_cols = [row[1] for row in cursor.fetchall()]

def _add_column_if_missing(col_name, col_def):
    if col_name not in existing_cols:
        cursor.execute(f"ALTER TABLE library ADD COLUMN {col_def}")
        existing_cols.append(col_name)

_add_column_if_missing('description', 'description TEXT')
_add_column_if_missing('price', 'price REAL')
_add_column_if_missing('rent_price', 'rent_price REAL')
_add_column_if_missing('file_path', 'file_path TEXT')

# Insert a sample record only if the table is empty
cursor.execute("SELECT COUNT(*) FROM library")
if cursor.fetchone()[0] == 0:
    cursor.execute(
        """
        INSERT INTO library (title,author,description,price,rent_price,file_path)
        VALUES (?,?,?,?,?,?)
        """,
        ('Python Basics', 'John Smith', 'Learn Python from scratch', 99, 29, 'books/python.pdf')
    )


cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    book_id INTEGER,
    type TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# ef708534664aff88064e8e6f98fffdaf6bca1265
# 0v23libRB75CSnnR73JA

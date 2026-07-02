import sqlite3

conn = sqlite3.connect("ecommerce.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    username TEXT,
    product TEXT,
    quantity INTEGER,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS wishlist (
    username TEXT,
    product TEXT,
    price INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER,
    name TEXT,
    price INTEGER,
    category TEXT,
    image TEXT
)
""")

conn.commit()
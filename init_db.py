import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "market.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS markets;
DROP TABLE IF EXISTS vendors;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;

CREATE TABLE markets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    market_id INTEGER
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    vendor_id INTEGER
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    quantity INTEGER
);

INSERT INTO markets (name, location) VALUES
('Downtown Farmers Market', 'Minneapolis'),
('Uptown Farmers Market', 'St Paul');

INSERT INTO vendors (name, market_id) VALUES
('Green Farm', 1),
('Fresh Fields', 1),
('Organic Hub', 2);

INSERT INTO products (name, price, vendor_id) VALUES
('Apples', 3.50, 1),
('Tomatoes', 2.75, 1),
('Milk', 4.00, 2),
('Honey', 6.00, 3);
""")

conn.commit()
conn.close()

print("Database initialized successfully")

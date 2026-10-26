
import random
import sqlite3
from datetime import date, timedelta

random.seed(42)

con = sqlite3.connect("source.db")

con.executescript("""
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    city TEXT,
    active_flag TEXT,
    updated_at TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    unit_price REAL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    updated_at TEXT
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
);
""")

countries = ["india", "usa", "germany"]
cities = ["Pune", "Austin", "Berlin", "Delhi"]

customers = [
    (
        i,
        f"   Customer {i}   ",
        random.choice(countries),
        random.choice(cities),
        random.choice("YYYN"),
        "2026-01-01",
    )
    for i in range(1, 201)
]

products = [
    (i, f"Product {i}", round(random.uniform(5, 200), 2))
    for i in range(1, 51)
]

con.executemany(
    "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)",
    customers,
)
con.executemany(
    "INSERT INTO products VALUES (?, ?, ?)",
    products,
)

start = date(2026, 1, 1)
orders = []
items = []

for order_id in range(1, 5001):
    order_date = (
        start + timedelta(days=random.randint(0, 89))
    ).isoformat()

    orders.append((
        order_id,
        random.randint(1, 200),
        order_date,
        order_date,
    ))

    for product_id in random.sample(
        range(1, 51),
        random.randint(1, 4),
    ):
        items.append((
            order_id,
            product_id,
            random.randint(1, 5),
        ))

con.executemany(
    "INSERT INTO orders VALUES (?, ?, ?, ?)",
    orders,
)
con.executemany(
    "INSERT INTO order_items VALUES (?, ?, ?)",
    items,
)

con.commit()

for table in ["customers", "products", "orders", "order_items"]:
    count = con.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]
    print(f"{table}: {count} rows")

con.close()
print("Source database created successfully.")

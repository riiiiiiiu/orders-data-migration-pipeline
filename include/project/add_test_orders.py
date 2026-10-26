
import sqlite3

con = sqlite3.connect("source.db")

try:
    # Add two new orders
    con.executemany(
        """
        INSERT INTO orders
            (order_id, customer_id, order_date, updated_at)
        VALUES (?, ?, ?, ?)
        """,
        [
            (5001, 1, "2026-04-01", "2026-04-01"),
            (5002, 2, "2026-04-02", "2026-04-02"),
        ],
    )

    # Add order items for the new orders
    con.executemany(
        """
        INSERT INTO order_items
            (order_id, product_id, quantity)
        VALUES (?, ?, ?)
        """,
        [
            (5001, 1, 2),
            (5001, 3, 1),
            (5002, 2, 4),
        ],
    )

    con.commit()
    print("Added 2 test orders and 3 order items.")

finally:
    con.close()

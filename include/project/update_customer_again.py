
import sqlite3

con = sqlite3.connect("source.db")

try:
    con.execute(
        """
        UPDATE customers
        SET name = ?, updated_at = ?
        WHERE customer_id = ?
        """,
        ("   Rehan Test Customer   ", "2026-04-10", 1),
    )

    con.commit()

    result = con.execute(
        "SELECT customer_id, name, updated_at "
        "FROM customers WHERE customer_id = 1"
    ).fetchone()

    print(f"Updated source record: {result}")

finally:
    con.close()

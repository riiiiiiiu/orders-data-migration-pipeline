
import sqlite3

con = sqlite3.connect("source.db")

try:
    customer_id = 1

    before = con.execute(
        "SELECT name FROM customers WHERE customer_id = ?",
        (customer_id,),
    ).fetchone()

    if before is None:
        raise ValueError(f"Customer {customer_id} not found")

    print(f"Previous source name: {before[0]!r}")

    con.execute(
        """
        UPDATE customers
        SET name = ?, updated_at = ?
        WHERE customer_id = ?
        """,
        ("   Updated Customer 1   ", "2026-04-03", customer_id),
    )

    con.commit()

    after = con.execute(
        "SELECT name, updated_at FROM customers WHERE customer_id = ?",
        (customer_id,),
    ).fetchone()

    print(f"Updated source name: {after[0]!r}")
    print(f"Updated timestamp: {after[1]}")
    print("Source customer update completed.")

finally:
    con.close()

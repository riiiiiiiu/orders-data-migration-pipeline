
import duckdb

DB_PATH = "warehouse.duckdb"

con = duckdb.connect(DB_PATH, read_only=True)

try:
    print("\nFIRST 10 TRANSFORMED CUSTOMERS")
    print("-" * 60)

    rows = con.execute("""
        SELECT
            customer_id,
            customer_name,
            country,
            city,
            updated_at
        FROM stg_customers
        ORDER BY customer_id
        LIMIT 10
    """).fetchall()

    for row in rows:
        print(row)

    total = con.execute(
        "SELECT COUNT(*) FROM stg_customers"
    ).fetchone()[0]

    print("-" * 60)
    print(f"Total customers: {total}")

    invalid_names = con.execute("""
        SELECT COUNT(*)
        FROM stg_customers
        WHERE customer_name != TRIM(customer_name)
    """).fetchone()[0]

    print(f"Names with extra spaces: {invalid_names}")

finally:
    con.close()

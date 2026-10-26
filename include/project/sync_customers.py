
import sqlite3
import duckdb
import pandas as pd

SOURCE_DB = "source.db"
WAREHOUSE_DB = "warehouse.duckdb"


def main():
    source = sqlite3.connect(SOURCE_DB)
    warehouse = duckdb.connect(WAREHOUSE_DB)

    try:
        source_df = pd.read_sql_query(
            "SELECT * FROM customers",
            source,
        )

        warehouse.register("source_customers", source_df)

        # Update only customers whose source data has changed
        warehouse.execute("""
            UPDATE customers AS target
            SET
                name = source.name,
                country = source.country,
                city = source.city,
                active_flag = source.active_flag,
                updated_at = source.updated_at
            FROM source_customers AS source
            WHERE target.customer_id = source.customer_id
              AND (
                  target.name IS DISTINCT FROM source.name
                  OR target.country IS DISTINCT FROM source.country
                  OR target.city IS DISTINCT FROM source.city
                  OR target.active_flag IS DISTINCT FROM source.active_flag
                  OR target.updated_at IS DISTINCT FROM source.updated_at
              )
        """)

        warehouse.unregister("source_customers")

        result = warehouse.execute("""
            SELECT customer_id, name, updated_at
            FROM customers
            WHERE customer_id = 1
        """).fetchone()

        print(f"Warehouse customer: {result}")

        count = warehouse.execute(
            "SELECT COUNT(*) FROM customers"
        ).fetchone()[0]

        print(f"Total warehouse customers: {count}")

    finally:
        warehouse.close()
        source.close()


if __name__ == "__main__":
    main()


import sqlite3
import duckdb
import pandas as pd

SOURCE_DB = "source.db"
WAREHOUSE_DB = "warehouse.duckdb"

TABLES = [
    "customers",
    "products",
    "orders",
    "order_items",
]


def main():
    source = sqlite3.connect(SOURCE_DB)

    try:
        for table in TABLES:
            df = pd.read_sql_query(
                f"SELECT * FROM {table}",
                source,
            )

            # Use a fresh DuckDB connection for each table
            warehouse = duckdb.connect(WAREHOUSE_DB)

            try:
                warehouse.execute(
                    f'CREATE OR REPLACE TABLE "{table}" AS '
                    "SELECT * FROM df"
                )

                count = warehouse.execute(
                    f'SELECT COUNT(*) FROM "{table}"'
                ).fetchone()[0]

                print(f"{table}: loaded {count} rows")

            finally:
                warehouse.close()

    finally:
        source.close()

    print("Extraction and loading completed successfully.")


if __name__ == "__main__":
    main()

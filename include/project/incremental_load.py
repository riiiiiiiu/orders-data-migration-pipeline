
import sqlite3
import duckdb
import pandas as pd

SOURCE_DB = "source.db"
WAREHOUSE_DB = "warehouse.duckdb"


def load_new_rows(source, warehouse, table, key_columns):
    source_df = pd.read_sql_query(
        f'SELECT * FROM "{table}"',
        source,
    )

    # Read existing key values from the warehouse
    existing_df = warehouse.execute(
        f'SELECT {", ".join(key_columns)} FROM "{table}"'
    ).fetchdf()

    # Build keys to identify rows already loaded
    if len(key_columns) == 1:
        existing_keys = set(existing_df[key_columns[0]])
        source_keys = source_df[key_columns[0]]
    else:
        existing_keys = set(
            existing_df[key_columns].itertuples(
                index=False, name=None
            )
        )
        source_keys = source_df[key_columns].apply(
            tuple, axis=1
        )

    new_rows = source_df[~source_keys.isin(existing_keys)]

    if new_rows.empty:
        print(f"{table}: no new rows")
        return

    warehouse.register("new_rows_df", new_rows)

    columns = ", ".join(
        f'"{column}"' for column in new_rows.columns
    )

    warehouse.execute(
        f'INSERT INTO "{table}" ({columns}) '
        f'SELECT {columns} FROM new_rows_df'
    )

    warehouse.unregister("new_rows_df")

    print(f"{table}: inserted {len(new_rows)} rows")


def main():
    source = sqlite3.connect(SOURCE_DB)
    warehouse = duckdb.connect(WAREHOUSE_DB)

    try:
        load_new_rows(
            source, warehouse, "orders", ["order_id"]
        )

        load_new_rows(
            source,
            warehouse,
            "order_items",
            ["order_id", "product_id"],
        )

        for table in ["orders", "order_items"]:
            count = warehouse.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]

            print(f"{table}: total {count} rows")

    finally:
        warehouse.close()
        source.close()


if __name__ == "__main__":
    main()

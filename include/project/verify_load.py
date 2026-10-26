
import sqlite3
import duckdb

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
    warehouse = duckdb.connect(WAREHOUSE_DB)

    all_passed = True

    try:
        print("\nDATA MIGRATION RECONCILIATION")
        print("-" * 65)

        for table in TABLES:
            source_count = source.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            target_count = warehouse.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]

            status = (
                "PASS"
                if source_count == target_count
                else "FAIL"
            )

            if status == "FAIL":
                all_passed = False

            print(
                f"{table:<15} "
                f"Source: {source_count:<7} "
                f"Target: {target_count:<7} "
                f"{status}"
            )

        print("-" * 65)

        if all_passed:
            print("RESULT: All tables passed reconciliation.")
        else:
            print("RESULT: Reconciliation failed.")

    finally:
        warehouse.close()
        source.close()


if __name__ == "__main__":
    main()

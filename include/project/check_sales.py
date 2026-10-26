
import duckdb

con = duckdb.connect("warehouse.duckdb", read_only=True)

try:
    checks = [
        (
            "Warehouse orders",
            "SELECT COUNT(*) FROM orders",
            5002,
        ),
        (
            "Warehouse order items",
            "SELECT COUNT(*) FROM order_items",
            12429,
        ),
        (
            "Sales fact rows",
            "SELECT COUNT(*) FROM fct_order_sales",
            12429,
        ),
        (
            "Distinct orders in sales fact",
            "SELECT COUNT(DISTINCT order_id) FROM fct_order_sales",
            5002,
        ),
        (
            "New order 5001 lines",
            "SELECT COUNT(*) FROM fct_order_sales WHERE order_id = 5001",
            2,
        ),
        (
            "New order 5002 lines",
            "SELECT COUNT(*) FROM fct_order_sales WHERE order_id = 5002",
            1,
        ),
    ]

    print("\nINCREMENTAL LOAD VALIDATION")
    print("-" * 65)

    all_passed = True

    for label, query, expected in checks:
        actual = con.execute(query).fetchone()[0]
        passed = actual == expected
        all_passed = all_passed and passed

        print(
            f"{label}: actual={actual}, expected={expected}, "
            f"{'PASS' if passed else 'FAIL'}"
        )

    print("-" * 65)
    print(
        "RESULT: "
        + ("All checks passed." if all_passed else "Validation failed.")
    )

finally:
    con.close()

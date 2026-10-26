
import duckdb

con = duckdb.connect("warehouse.duckdb", read_only=True)

try:
    print("\nCUSTOMER SALES SUMMARY VALIDATION")
    print("-" * 55)

    summary = con.execute("""
        SELECT
            COUNT(*) AS customer_count,
            SUM(total_orders) AS customer_order_count,
            SUM(total_units_purchased) AS total_units,
            ROUND(SUM(total_sales), 2) AS summary_sales
        FROM mart_customer_sales
    """).fetchone()

    fact = con.execute("""
        SELECT
            COUNT(DISTINCT customer_id),
            COUNT(DISTINCT order_id),
            SUM(quantity),
            ROUND(SUM(line_total), 2)
        FROM fct_order_sales
    """).fetchone()

    labels = [
        "Customers with orders",
        "Distinct orders",
        "Total units purchased",
        "Total sales",
    ]

    passed = True

    for label, summary_value, fact_value in zip(
        labels, summary, fact
    ):
        match = summary_value == fact_value

        if not match:
            passed = False

        print(
            f"{label}: summary={summary_value}, "
            f"fact={fact_value}, "
            f"{'PASS' if match else 'FAIL'}"
        )

    print("-" * 55)
    print(
        "RESULT: "
        + (
            "All reconciliation checks passed."
            if passed
            else "Reconciliation failed."
        )
    )

finally:
    con.close()

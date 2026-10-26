
SELECT
    customer_id,
    customer_name,
    country,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_purchased,
    CAST(SUM(line_total) AS DECIMAL(14, 2)) AS total_sales,
    CAST(AVG(line_total) AS DECIMAL(12, 2)) AS avg_order_line_value
FROM fct_order_sales
GROUP BY
    customer_id,
    customer_name,
    country

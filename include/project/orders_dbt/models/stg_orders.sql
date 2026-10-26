
SELECT
    order_id,
    customer_id,
    CAST(order_date AS DATE) AS order_date,
    CAST(updated_at AS DATE) AS updated_at
FROM orders


SELECT
    oi.order_id,
    o.order_date,
    o.customer_id,
    c.customer_name,
    c.country,
    oi.product_id,
    p.product_name,
    oi.quantity,
    p.unit_price,
    CAST(oi.quantity * p.unit_price AS DECIMAL(12, 2))
        AS line_total
FROM stg_order_items AS oi
INNER JOIN stg_orders AS o
    ON oi.order_id = o.order_id
INNER JOIN stg_customers AS c
    ON o.customer_id = c.customer_id
INNER JOIN stg_products AS p
    ON oi.product_id = p.product_id

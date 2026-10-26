
SELECT
    order_id,
    product_id,
    CAST(quantity AS INTEGER) AS quantity
FROM order_items

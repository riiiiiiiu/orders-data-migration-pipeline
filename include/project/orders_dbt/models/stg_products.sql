
SELECT
    product_id,
    TRIM(product_name) AS product_name,
    CAST(unit_price AS DECIMAL(10, 2)) AS unit_price
FROM products

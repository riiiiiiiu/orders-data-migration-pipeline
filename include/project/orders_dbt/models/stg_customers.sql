
SELECT
    customer_id,
    TRIM(name) AS customer_name,
    UPPER(TRIM(country)) AS country,
    TRIM(city) AS city,
    active_flag,
    CAST(updated_at AS DATE) AS updated_at
FROM customers

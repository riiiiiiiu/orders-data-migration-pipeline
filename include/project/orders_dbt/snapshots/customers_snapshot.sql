
{% snapshot customers_snapshot %}

{{
    config(
        target_schema='main',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}

SELECT
    customer_id,
    TRIM(name) AS customer_name,
    UPPER(TRIM(country)) AS country,
    TRIM(city) AS city,
    active_flag,
    CAST(updated_at AS TIMESTAMP) AS updated_at
FROM customers

{% endsnapshot %}

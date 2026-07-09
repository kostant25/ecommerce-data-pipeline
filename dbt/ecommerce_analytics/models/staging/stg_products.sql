SELECT
    product_id,
    category,
    subcategory,
    product_name,
    base_price
FROM {{ source('raw', 'dim_products') }}
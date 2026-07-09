SELECT
    cart_id,
    cart_item_id,
    product_id,
    quantity,
    added_time
FROM {{ source('raw', 'fct_cart_items') }}
SELECT
    order_id,
    cart_id,
    user_id,
    order_time,
    status
FROM {{ source('raw', 'fct_orders') }}
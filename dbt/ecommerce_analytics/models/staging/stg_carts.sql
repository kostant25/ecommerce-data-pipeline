SELECT
    cart_id,
    user_id,
    session_id,
    created_time
FROM {{ source('raw', 'fct_carts') }}
WITH cart_items as (
    SELECT
        sci.cart_id,
        sci.quantity,
        sp.base_price as price
    FROM {{ ref('stg_cart_items') }} sci
    JOIN {{ ref('stg_products') }} sp ON sci.product_id = sp.product_id
),
carts as (
    SELECT
        sc.cart_id,
        sc.user_id,
        SUM(ci.quantity * ci.price) as amount,
        sc.created_time             as cart_created_time
    FROM {{ ref('stg_carts') }} sc
    JOIN cart_items ci ON sc.cart_id = ci.cart_id
    GROUP BY sc.cart_id, sc.user_id, sc.created_time
),
carts_with_user as (
    SELECT
        c.cart_id,
        su.user_id,
        su.name,
        su.email,
        su.registration_date,
        su.city,
        su.state,
        c.cart_created_time,
        c.amount
    FROM carts c
    JOIN {{ ref('stg_users') }} su ON c.user_id = su.user_id
)
SELECT
    so.order_id,
    so.order_time,
    so.status,
    cwu.cart_id,
    cwu.cart_created_time,
    cwu.amount,
    cwu.user_id,
    cwu.name,
    cwu.email,
    cwu.registration_date,
    cwu.city,
    cwu.state
FROM {{ ref('stg_orders') }} so
JOIN carts_with_user cwu ON so.cart_id = cwu.cart_id

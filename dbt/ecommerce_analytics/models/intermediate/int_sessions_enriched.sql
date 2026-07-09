WITH sessions_with_cart as (
    SELECT
        ss.session_id,
        ss.user_id,
        ss.start_time,
        ss.end_time,
        ss.device_type,
        ss.utm_source,
        sc.cart_id,
        sc.created_time AS cart_created_time
    FROM {{ ref('stg_sessions') }} ss
    LEFT JOIN {{ ref('stg_carts') }} sc ON ss.session_id = sc.session_id
),
sessions_with_order as (
    SELECT
        swc.*,
        so.order_id,
        so.order_time,
        so.status
    FROM sessions_with_cart swc
    LEFT JOIN {{ ref('stg_orders') }} so ON swc.cart_id = so.cart_id
)
SELECT
    session_id,
    user_id,
    start_time,
    end_time,
    device_type,
    utm_source,
    cart_id IS NOT NULL AS has_cart,
    order_id IS NOT NULL AS has_order,
    status AS order_status,
    order_time,
    cart_created_time
FROM sessions_with_order

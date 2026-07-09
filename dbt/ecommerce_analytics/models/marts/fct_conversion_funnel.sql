WITH total AS (
    SELECT
        DATE_TRUNC('week', start_time) AS week,
        COUNT(DISTINCT session_id) AS total_sessions,
        COUNT(*) FILTER (WHERE has_cart) AS total_carts,
        COUNT(*) FILTER (WHERE has_order) AS total_orders,
        COUNT(*) FILTER (WHERE order_status = 'delivered') AS total_paid
    FROM {{ ref('int_sessions_enriched') }}
    GROUP BY DATE_TRUNC('week', start_time)
)
SELECT
    week,
    total_sessions,
    total_carts,
    total_orders,
    total_paid,
    CASE
        WHEN total_sessions > 0
        THEN ROUND(total_carts::decimal / total_sessions * 100, 2)
    END AS cart_conversion_rate,
    CASE
        WHEN total_carts > 0
        THEN ROUND(total_orders::decimal / total_carts * 100, 2)
    END AS order_conversion_rate,
    CASE
        WHEN total_orders > 0
        THEN ROUND(total_paid::decimal / total_orders * 100, 2)
    END AS paid_conversion_rate
FROM total
ORDER BY week

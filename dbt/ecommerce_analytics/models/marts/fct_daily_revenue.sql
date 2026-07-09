SELECT
    DATE(order_time) as order_date,
    SUM(amount) as daily_revenue,
    SUM(SUM(amount)) OVER (ORDER BY DATE(order_time)) AS cumulative_revenue
FROM {{ ref('int_orders_enriched') }}
WHERE status = 'delivered'
GROUP BY DATE(order_time)
ORDER BY order_date
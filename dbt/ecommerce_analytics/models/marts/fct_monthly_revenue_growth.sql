WITH month_revenue AS (
    SELECT
        DATE_TRUNC('month', order_time) as order_month,
        SUM(amount) as monthly_revenue,
        LAG(SUM(amount), 1) OVER (ORDER BY DATE_TRUNC('month', order_time)) as previous_revenue
    FROM {{ ref('int_orders_enriched') }}
    WHERE status = 'delivered'
    GROUP BY DATE_TRUNC('month', order_time)
)
SELECT
    order_month,
    monthly_revenue,
    previous_revenue,
    ROUND((monthly_revenue - previous_revenue) / previous_revenue * 100, 2) as growth_percent
FROM month_revenue
ORDER BY order_month
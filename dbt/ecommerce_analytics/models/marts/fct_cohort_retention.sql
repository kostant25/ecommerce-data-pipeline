WITH first_orders AS (
    SELECT
        MIN(DATE_TRUNC('month', order_time)) AS first_order_month,
        user_id
    FROM {{ ref('int_orders_enriched') }}
    WHERE status = 'delivered'
    GROUP BY user_id
), cohort_months AS (
    SELECT
        DATE_TRUNC('month', order_time) AS cohort_month,
        user_id
    FROM {{ ref('int_orders_enriched') }}
    WHERE status = 'delivered'
), cohort_sizes AS (
    SELECT
        first_order_month,
        COUNT(DISTINCT user_id) AS cohort_size
    FROM first_orders
    GROUP BY first_order_month
)

SELECT
    TO_CHAR(fo.first_order_month, 'YYYY-MM') AS cohort_month,
    (DATE_PART('year', cm.cohort_month) - DATE_PART('year', fo.first_order_month)) * 12 + (DATE_PART('month', cm.cohort_month) - DATE_PART('month', fo.first_order_month)) AS period_index,
    COUNT(DISTINCT cm.user_id) AS active_customers,
    cs.cohort_size,
    ROUND((COUNT(DISTINCT cm.user_id)::DECIMAL / cs.cohort_size) * 100, 2) AS retention_rate
FROM cohort_months cm
JOIN first_orders fo ON cm.user_id = fo.user_id
JOIN cohort_sizes cs ON fo.first_order_month = cs.first_order_month
GROUP BY fo.first_order_month, period_index, cs.cohort_size
ORDER BY cohort_month, period_index

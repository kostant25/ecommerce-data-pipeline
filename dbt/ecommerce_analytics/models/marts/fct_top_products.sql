WITH cart_items AS (
    SELECT
        sci.cart_id,
        sp.category,
        sp.product_name,
        sp.base_price * sci.quantity AS amount
    FROM {{ ref('stg_cart_items') }} sci
    JOIN {{ ref('stg_products') }} sp ON sci.product_id = sp.product_id
),
delivered_items AS (
    SELECT
        ci.category,
        ci.product_name,
        ci.amount
    FROM cart_items ci
    JOIN {{ ref('int_orders_enriched') }} ioe ON ci.cart_id = ioe.cart_id
    WHERE ioe.status = 'delivered'
),
product_revenue AS (
    SELECT
        category,
        product_name,
        SUM(amount) AS total_revenue
    FROM delivered_items
    GROUP BY category, product_name
),
ranked_products AS (
    SELECT
        category,
        product_name,
        total_revenue,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank
    FROM product_revenue
)
SELECT
    category,
    product_name,
    total_revenue,
    rank
FROM ranked_products
WHERE rank <= 5
ORDER BY category, rank
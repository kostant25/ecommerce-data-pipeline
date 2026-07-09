SELECT
    payment_id,
    order_id,
    amount,
    payment_time,
    method
FROM {{ source('raw', 'fct_payments') }}
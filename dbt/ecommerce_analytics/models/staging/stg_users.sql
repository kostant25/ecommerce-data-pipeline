SELECT
    user_id,
    name,
    email,
    registration_date,
    city,
    state
FROM {{ source('raw', 'dim_users') }}
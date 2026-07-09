SELECT
    session_id,
    user_id,
    start_time,
    end_time,
    device_type,
    utm_source
FROM {{ source('raw', 'fct_sessions') }}
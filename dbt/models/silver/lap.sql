{{ config(
    materialized='incremental',
    unique_key='id'
) }}

SELECT 
    (lap->>'id')::bigint AS id,
    ad.id AS activity_id,
    (lap->>'split')::int AS split,
    (lap->>'distance')::numeric AS distance,
    (lap->>'moving_time')::interval AS moving_time,
    (lap->>'elapsed_time')::interval AS elapsed_time,
    (lap->>'average_speed')::numeric AS average_speed,
    (lap->>'average_watts')::numeric AS average_watts,
    (lap->>'max_speed')::numeric AS max_speed,
    (lap->>'total_elevation_gain')::numeric AS total_elevation_gain,
    (lap->>'start_date')::timestamptz AS start_date
FROM 
    {{ source('strava_bronze', 'activities_detailed') }} ad
CROSS JOIN LATERAL 
    jsonb_array_elements(ad.raw_data->'laps') AS lap
{% if is_incremental() %}
WHERE (lap->>'start_date')::timestamptz >
    (SELECT COALESCE(MAX(start_date), '1970-01-01') FROM {{ this }})
{% endif %}

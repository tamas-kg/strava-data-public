{{ config(
    materialized='incremental',
    unique_key=['activity_id', 'split']
) }}

SELECT 
    ad.id AS activity_id,
    (s->>'split')::int AS split,
    (s->>'distance')::numeric AS distance,
    (s->>'moving_time')::interval AS moving_time,
    (s->>'elapsed_time')::interval AS elapsed_time,
    (s->>'average_speed')::numeric AS average_speed,
    (s->>'elevation_difference')::numeric AS elevation_difference,
    (ad.raw_data->>'start_date')::timestamptz AS start_date  -- used only for incremental filtering
FROM 
    {{ source('strava_bronze', 'activities_detailed') }} ad
CROSS JOIN LATERAL 
    jsonb_array_elements(ad.raw_data->'splits_metric') AS s
{% if is_incremental() %}
WHERE (ad.raw_data->>'start_date')::timestamptz >
    (SELECT COALESCE(MAX(start_date), '1970-01-01') FROM {{ this }})
{% endif %}

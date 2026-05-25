{{ config(
    materialized='incremental',
    unique_key='id'
) }}

SELECT 
    (seg->>'id')::bigint AS id,
    ad.id AS activity_id,
    (seg->'segment'->>'id')::bigint AS segment_id,
    seg->>'name' AS name,
    (seg->>'distance')::numeric AS distance,
    (seg->>'moving_time')::interval AS moving_time,
    (seg->>'elapsed_time')::interval AS elapsed_time,
    (seg->>'pr_rank')::int AS pr_rank,
    (seg->>'start_date')::timestamptz AS start_date,
    (seg->>'start_date_local')::timestamptz AS start_date_local,
    (seg->>'device_watts')::boolean AS device_watts,
    (seg->>'start_index')::int AS start_index,
    (seg->>'end_index')::int AS end_index,
    seg->'segment'->>'city' AS segment_city,
    seg->'segment'->>'country' AS segment_country,
    (seg->'segment'->>'average_grade')::numeric AS average_grade,
    (seg->'segment'->>'maximum_grade')::numeric AS maximum_grade,
    (seg->'segment'->>'elevation_low')::numeric AS elevation_low,
    (seg->'segment'->>'elevation_high')::numeric AS elevation_high
FROM 
    {{ source('strava_bronze', 'activities_detailed') }} ad
CROSS JOIN LATERAL 
    jsonb_array_elements(ad.raw_data->'segment_efforts') AS seg
{% if is_incremental() %}
WHERE (seg->>'start_date')::timestamptz >
    (SELECT COALESCE(MAX(start_date), '1970-01-01') FROM {{ this }})
{% endif %}

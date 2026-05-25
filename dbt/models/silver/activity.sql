{{ config(
    materialized='incremental',
    unique_key='id'
) }}

  SELECT
    ad.id,
    ad.raw_data->>'name' AS name,
    ad.raw_data->>'type' AS activity_type,
    (ad.raw_data->>'start_date')::timestamptz AS start_date,
    (ad.raw_data->>'distance')::numeric AS distance,
    (ad.raw_data->>'moving_time')::interval AS moving_time,
    (ad.raw_data->>'elapsed_time')::interval AS elapsed_time,
    (ad.raw_data->>'calories')::numeric AS calories,
    (ad.raw_data->>'pr_count')::numeric AS pr_count,
    ad.raw_data->>'description' AS description,
    ad.raw_data->'map'->>'id' AS map_id,
    ad.raw_data->'map'->>'polyline' AS polyline,
    ad.raw_data->>'summary_polyline' AS summary_polyline,
    (ad.raw_data->'start_latlng'->>0)::numeric AS start_lat,
    (ad.raw_data->'start_latlng'->>1)::numeric AS start_lng,
    (ad.raw_data->'end_latlng'->>0)::numeric AS end_lat,
    (ad.raw_data->'end_latlng'->>1)::numeric AS end_lng,
    ad.raw_data->>'device_name' AS device_name,
    ST_SetSRID(
      ST_LineFromEncodedPolyline(ad.raw_data->'map'->>'polyline', 5),
      4326
    ) AS route_geom
  FROM {{ source('strava_bronze', 'activities_detailed') }} ad

  {% if is_incremental() %}
  WHERE (ad.raw_data->>'start_date')::timestamptz >
    (SELECT COALESCE(MAX(start_date), '1970-01-01') FROM {{ this }})
  {% endif %}


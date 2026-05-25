INSERT INTO strava_silver.split_metric (
  activity_id, split, distance, moving_time, elapsed_time,
  average_speed, elevation_difference
)
SELECT
  ad.id,
  (s->>'split')::int,
  (s->>'distance')::numeric,
  (s->>'moving_time')::interval,
  (s->>'elapsed_time')::interval,
  (s->>'average_speed')::numeric,
  (s->>'elevation_difference')::numeric
FROM strava_bronze.activities_detailed ad
CROSS JOIN LATERAL jsonb_array_elements(ad.raw_data->'splits_metric') AS s
ON CONFLICT (activity_id, split) DO UPDATE
SET
  distance = EXCLUDED.distance,
  moving_time = EXCLUDED.moving_time,
  elapsed_time = EXCLUDED.elapsed_time,
  average_speed = EXCLUDED.average_speed,
  elevation_difference = EXCLUDED.elevation_difference;
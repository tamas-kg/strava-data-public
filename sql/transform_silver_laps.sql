INSERT INTO strava_silver.lap (
  id, activity_id, split, distance, moving_time, elapsed_time,
  average_speed, average_watts, max_speed, total_elevation_gain, start_date
)
SELECT
  (lap->>'id')::bigint,
  ad.id,
  (lap->>'split')::int,
  (lap->>'distance')::numeric,
  (lap->>'moving_time')::interval,
  (lap->>'elapsed_time')::interval,
  (lap->>'average_speed')::numeric,
  (lap->>'average_watts')::numeric,
  (lap->>'max_speed')::numeric,
  (lap->>'total_elevation_gain')::numeric,
  (lap->>'start_date')::timestamptz
FROM strava_bronze.activities_detailed ad
CROSS JOIN LATERAL jsonb_array_elements(ad.raw_data->'laps') AS lap
ON CONFLICT (id) DO UPDATE
SET
  distance = EXCLUDED.distance,
  moving_time = EXCLUDED.moving_time,
  elapsed_time = EXCLUDED.elapsed_time,
  average_speed = EXCLUDED.average_speed,
  average_watts = EXCLUDED.average_watts,
  max_speed = EXCLUDED.max_speed,
  total_elevation_gain = EXCLUDED.total_elevation_gain,
  start_date = EXCLUDED.start_date;
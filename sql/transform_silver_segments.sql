INSERT INTO strava_silver.segment_effort (
  id, activity_id, segment_id, name, distance, moving_time, elapsed_time,
  pr_rank, start_date, start_date_local, device_watts,
  start_index, end_index, segment_city, segment_country,
  average_grade, maximum_grade, elevation_low, elevation_high
)
SELECT
  (seg->>'id')::bigint,
  ad.id,
  (seg->'segment'->>'id')::bigint,
  seg->>'name',
  (seg->>'distance')::numeric,
  (seg->>'moving_time')::interval,
  (seg->>'elapsed_time')::interval,
  (seg->>'pr_rank')::int,
  (seg->>'start_date')::timestamptz,
  (seg->>'start_date_local')::timestamptz,
  (seg->>'device_watts')::boolean,
  (seg->>'start_index')::int,
  (seg->>'end_index')::int,
  seg->'segment'->>'city',
  seg->'segment'->>'country',
  (seg->'segment'->>'average_grade')::numeric,
  (seg->'segment'->>'maximum_grade')::numeric,
  (seg->'segment'->>'elevation_low')::numeric,
  (seg->'segment'->>'elevation_high')::numeric
FROM strava_bronze.activities_detailed ad
CROSS JOIN LATERAL jsonb_array_elements(ad.raw_data->'segment_efforts') AS seg
WHERE (seg->>'start_date')::timestamptz > (
  SELECT COALESCE(MAX(start_date), '1970-01-01') FROM strava_silver.segment_effort
)
ON CONFLICT (id) DO UPDATE
SET
  distance = EXCLUDED.distance,
  moving_time = EXCLUDED.moving_time,
  elapsed_time = EXCLUDED.elapsed_time,
  pr_rank = EXCLUDED.pr_rank,
  start_date = EXCLUDED.start_date,
  start_date_local = EXCLUDED.start_date_local,
  device_watts = EXCLUDED.device_watts,
  start_index = EXCLUDED.start_index,
  end_index = EXCLUDED.end_index,
  segment_city = EXCLUDED.segment_city,
  segment_country = EXCLUDED.segment_country,
  average_grade = EXCLUDED.average_grade,
  maximum_grade = EXCLUDED.maximum_grade,
  elevation_low = EXCLUDED.elevation_low,
  elevation_high = EXCLUDED.elevation_high;
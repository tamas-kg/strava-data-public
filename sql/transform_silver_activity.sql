INSERT INTO strava_silver.activity (
  id, name, activity_type, start_date, distance, moving_time, elapsed_time,
  calories, pr_count, description, map_id, polyline, summary_polyline,
  start_lat, start_lng, end_lat, end_lng,
  device_name, route_geom
)
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
FROM strava_bronze.activities_detailed ad
WHERE (ad.raw_data->>'start_date')::timestamptz > (
  SELECT COALESCE(MAX(start_date), '1970-01-01') FROM strava_silver.activity
)
ON CONFLICT (id) DO UPDATE
SET
  name = EXCLUDED.name,
  activity_type = EXCLUDED.activity_type,
  start_date = EXCLUDED.start_date,
  distance = EXCLUDED.distance,
  moving_time = EXCLUDED.moving_time,
  elapsed_time = EXCLUDED.elapsed_time,
  map_id = EXCLUDED.map_id,
  polyline = EXCLUDED.polyline,
  summary_polyline = EXCLUDED.summary_polyline,
  start_lat = EXCLUDED.start_lat,
  start_lng = EXCLUDED.start_lng,
  end_lat = EXCLUDED.end_lat,
  end_lng = EXCLUDED.end_lng,
  device_name = EXCLUDED.device_name,
  route_geom = EXCLUDED.route_geom;
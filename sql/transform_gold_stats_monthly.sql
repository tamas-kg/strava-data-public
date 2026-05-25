DELETE FROM strava_gold.monthly_stats;

INSERT INTO strava_gold.monthly_stats (
  year,
  month,
  total_distance,
  total_time,
  total_elevation,
  total_calories,
  total_prs
  )
SELECT
  EXTRACT(YEAR FROM a.start_date)::INT AS year,
  EXTRACT(MONTH FROM a.start_date)::INT AS month,
  ROUND(SUM(a.distance)/1000,1) AS total_distance,
  SUM(a.moving_time) AS total_time,
  SUM(l.total_elevation_gain) AS total_elevation,
  SUM(a.calories) AS total_calories,
  SUM(a.pr_count) AS total_prs
FROM strava_silver.activity a 
LEFT JOIN (
    SELECT activity_id, SUM(total_elevation_gain) AS total_elevation_gain
    FROM strava_silver.lap 
    GROUP BY activity_id) l 
ON a.id = l.activity_id
WHERE a.activity_type='Ride'
GROUP BY year, month
ORDER BY year, month;
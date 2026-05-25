CREATE TABLE IF NOT EXISTS strava_bronze.activities ( 
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    start_date TIMESTAMP,
    distance FLOAT,
    duration INTERVAL,
    activity_type VARCHAR(50),
    raw_data JSONB
);

CREATE TABLE IF NOT EXISTS strava_bronze.activities_detailed ( 
    id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    start_date TIMESTAMP,
    distance FLOAT,
    duration INTERVAL,
    activity_type VARCHAR(50),
    raw_data JSONB
);

CREATE TABLE IF NOT EXISTS strava_bronze.starred_segments (
    segment_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    distance FLOAT,  -- in meters
    activity_type VARCHAR(50),
    raw_data JSONB
);

CREATE TABLE IF NOT EXISTS strava_silver.activity (
  id BIGINT PRIMARY KEY,
  name TEXT,
  activity_type TEXT,
  start_date TIMESTAMPTZ,
  distance NUMERIC,
  moving_time INTERVAL,
  elapsed_time INTERVAL,
  calories NUMERIC,
  pr_count NUMERIC,
  description TEXT,
  map_id TEXT,
  polyline TEXT,
  summary_polyline TEXT,
  start_lat NUMERIC,
  start_lng NUMERIC,
  end_lat NUMERIC,
  end_lng NUMERIC,
  device_name TEXT,
  route_geom GEOMETRY(LineString, 4326)
);

CREATE TABLE IF NOT EXISTS strava_silver.lap (
  id BIGINT PRIMARY KEY,
  activity_id BIGINT NOT NULL REFERENCES strava_silver.activity(id),
  split INTEGER,
  distance NUMERIC,
  moving_time INTERVAL,
  elapsed_time INTERVAL,
  average_speed NUMERIC,
  average_watts NUMERIC,
  max_speed NUMERIC,
  total_elevation_gain NUMERIC,
  start_date TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS strava_silver.split_metric (
  activity_id BIGINT NOT NULL REFERENCES strava_silver.activity(id),
  split INTEGER,
  distance NUMERIC,
  moving_time INTERVAL,
  elapsed_time INTERVAL,
  average_speed NUMERIC,
  elevation_difference NUMERIC,
  PRIMARY KEY (activity_id, split)
);

CREATE TABLE IF NOT EXISTS strava_silver.segment_effort (
  id BIGINT PRIMARY KEY,
  activity_id BIGINT NOT NULL REFERENCES strava_silver.activity(id),
  segment_id BIGINT,
  name TEXT,
  distance NUMERIC,
  moving_time INTERVAL,
  elapsed_time INTERVAL,
  pr_rank INTEGER,
  start_date TIMESTAMPTZ,
  start_date_local TIMESTAMPTZ,
  device_watts BOOLEAN,
  start_index INTEGER,
  end_index INTEGER,
  segment_geom GEOMETRY(LineString, 4326),
  segment_city TEXT,
  segment_country TEXT,
  average_grade NUMERIC,
  maximum_grade NUMERIC,
  elevation_low NUMERIC,
  elevation_high NUMERIC
);

CREATE TABLE IF NOT EXISTS strava_gold.monthly_stats (
  year                INTEGER    NOT NULL,
  month               INTEGER    NOT NULL,
  total_distance      NUMERIC,
  total_time          INTERVAL,
  total_elevation     NUMERIC,
  total_calories      NUMERIC,
  total_prs           INTEGER
);

CREATE TABLE IF NOT EXISTS strava_gold.yearly_stats (
  month               INTEGER    NOT NULL,
  total_distance      NUMERIC,
  total_time          INTERVAL,
  total_elevation     NUMERIC,
  total_calories      NUMERIC,
  total_prs           INTEGER
);
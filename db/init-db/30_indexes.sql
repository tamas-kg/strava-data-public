CREATE INDEX idx_activity_route_geom
  ON strava_silver.activity
  USING GIST(route_geom);

CREATE INDEX idx_lap_activity
  ON strava_silver.lap(activity_id);

CREATE INDEX idx_split_metric_activity
  ON strava_silver.split_metric(activity_id, split);

CREATE INDEX idx_segment_effort_activity
  ON strava_silver.segment_effort(activity_id);

CREATE INDEX idx_segment_effort_segment_geom
  ON strava_silver.segment_effort
  USING GIST(segment_geom);
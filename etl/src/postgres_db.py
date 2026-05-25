import psycopg2
from datetime import datetime
import json

class PostgresDB:
    def __init__(self, db_name:str, db_user:str, db_password:str, db_host:str, db_port:int):
        self.conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        self.cursor = self.conn.cursor()
    
    def insert_activity(self, activity_data:dict, table:str) -> None:
        """Insert activity data into the PostgreSQL database."""

        insert_query = f"""
        INSERT INTO {table} (id, name, start_date, distance, duration, activity_type, raw_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        self.cursor.execute(insert_query, (
            activity_data['id'],
            activity_data['name'],
            datetime.fromisoformat(activity_data['start_date'].replace('Z', '+00:00')),
            activity_data['distance'],
            f'{activity_data["elapsed_time"]} seconds',  # Duration in seconds
            activity_data['type'],
            json.dumps(activity_data)
        ))
        self.conn.commit()

    def retrieve_activity_ids(self) -> list:
        select_query = """
                    SELECT DISTINCT a.id
                    FROM strava_bronze.activities a
                    LEFT JOIN strava_bronze.activities_detailed b ON a.id = b.id
                    WHERE b.id IS NULL;
                    """
        self.cursor.execute(select_query)
        ids = self.cursor.fetchall()
        
        return [id[0] for id in ids]

    def insert_starred_segment(self, segment_data:dict) -> None:
        """Insert starred segment data into the PostgreSQL database."""
        insert_query = """
        INSERT INTO strava_bronze.starred_segments (segment_id, name, distance, activity_type, raw_data)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (segment_id) DO NOTHING;
        """
        self.cursor.execute(insert_query, (
            segment_data['id'],
            segment_data['name'],
            segment_data['distance'],
            segment_data['activity_type'],
            json.dumps(segment_data)
        ))
        self.conn.commit()

    def retrieve_segment_effort_data(self):
        select_query = """
                    SELECT a.segment_id, a.name, a.start_date, a.elapsed_time
                    FROM strava_silver.segment_effort a 
                    INNER JOIN strava_bronze.starred_segments b
                    ON a.segment_id = b.segment_id
                    ORDER BY start_date desc;
                    """
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        
        return data, colnames
    
    def retrieve_map_data(self):
        select_query = """
                    SELECT ST_AsGeoJSON(
                    ST_LineFromEncodedPolyline(polyline)) AS geojson_geom,
                    ST_AsText(ST_GeomFromEWKB(decode(route_geom,'hex'))) AS route_geom
                    FROM strava_silver.activity
                    WHERE activity_type='Ride';
                    """
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]
        
        return data, colnames

    def retrieve_gold_monthly(self):
        select_query = """
                        SELECT 
                            year,
                            month,
                            TO_CHAR(DATE_TRUNC('month', make_date(year, month, 1)), 'YYYY-MM') AS year_month,
                            TO_CHAR(DATE_TRUNC('month', make_date(year, month, 1)), 'Mon') AS month_name,
                            month AS month_num,
                            total_distance,
                            total_time,
                            total_elevation,
                            total_calories,
                            total_prs
                        FROM strava_gold.monthly_stats
                        WHERE year >= EXTRACT(YEAR FROM CURRENT_DATE) - 1
                        ORDER BY year, month;
                    """
        self.cursor.execute(select_query)
        data = self.cursor.fetchall()
        colnames = [desc[0] for desc in self.cursor.description]

        return data, colnames

    def close(self):
        """Close the database connection."""
        self.cursor.close()
        self.conn.close()

from sqlalchemy import text
from app.core.database import engine


class SegmentsRepository:

    def get_efforts(self):

        query = text("""
            SELECT a.segment_id, a.name, a.start_date, a.elapsed_time
                    FROM public_strava_silver.segment_effort a 
                    INNER JOIN strava_bronze.starred_segments b
                    ON a.segment_id = b.segment_id
                    ORDER BY start_date desc;
            """)

        with engine.connect() as conn:
            result = conn.execute(query)

            return [
                dict(row._mapping)
                for row in result
            ]
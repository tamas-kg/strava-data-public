from sqlalchemy import text
from app.core.database import engine


class StatsRepository:

    def get_monthly_stats(self):

        query = text("""
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
            FROM public_strava_gold.monthly_stats
            WHERE year >= EXTRACT(YEAR FROM CURRENT_DATE) - 1
            ORDER BY year, month;
        """)

        with engine.connect() as conn:
            result = conn.execute(query)

            return [
                dict(row._mapping)
                for row in result
            ]
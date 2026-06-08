from sqlalchemy import text
from app.core.database import engine


class RoutesRepository:

    def get_routes(self):

        query = text("""
            SELECT ST_AsGeoJSON(
                ST_LineFromEncodedPolyline(polyline)) AS geojson_geom,
                ST_AsText(ST_GeomFromEWKB(decode(route_geom,'hex'))) AS route_geom
            FROM public_strava_silver.activity
            WHERE activity_type='Ride';
        """)

        with engine.connect() as conn:
            result = conn.execute(query)

            return [
                dict(row._mapping)
                for row in result
            ]
from src.strava_fetcher import StravaFetcher
from src.postgres_db import PostgresDB
from src.activity_processor import ActivityProcessor
from src.starred_segment_processor import StarredSegmentProcessor
from src.logger import setup_logger
from src.config import CLIENT_ID, CLIENT_SECRET, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

logger = setup_logger("BronzeLoad")

def main():

    # Initialize StravaFetcher with API access token and athlete ID
    strava_fetcher = StravaFetcher(CLIENT_ID,CLIENT_SECRET)
    
    # Initialize PostgresDB instance
    postgres_db = PostgresDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    
    # Initialize processors
    activity_processor = ActivityProcessor(db=postgres_db, api=strava_fetcher)
    starred_segment_processor = StarredSegmentProcessor(db=postgres_db)
    
    try:
        headers = strava_fetcher.refresh_api_token()
        # Fetch and process activities from Strava
        logger.info("Fetching activities from Strava...")
        activities = strava_fetcher.get_activities(headers)
        logger.info("Processing activities", extra={"count": len(activities)})
        activity_processor.process_activities(activities)
        
        # Fetch and process starred segments from Strava
        logger.info("Fetching starred segments from Strava...")
        starred_segments = strava_fetcher.get_starred_segments(headers)
        logger.info("Processing starred segments", extra={"count": len(starred_segments)})
        starred_segment_processor.process_starred_segments(starred_segments)

        activity_processor.process_detailed_activities()

    except Exception as e:
        logger.exception("An unexpected error occurred")
    
    finally:
        # Close the database connection
        postgres_db.close()
        logger.info("Database connection closed")

if __name__ == "__main__":
    main()

from src.postgres_db import PostgresDB
from src.strava_fetcher import StravaFetcher
from src.logger import setup_logger
import time

logger = setup_logger("ActivityProcessor")

class ActivityProcessor:
    def __init__(self, db: PostgresDB, api:StravaFetcher):
        self.db = db
        self.api = api

    def process_activities(self, activities) -> None:
        """Process and insert activities into the database."""
        for activity in activities:
            # For now, just filter out activities with no distance or duration
            if activity['distance'] > 0 and activity['elapsed_time'] > 0:
                self.db.insert_activity(activity,"strava_bronze.activities")
        logger.info("Processed activities", extra={"count": len(activities)})

    def process_detailed_activities(self) -> None:
        activity_ids = self.db.retrieve_activity_ids()
        count = 0
        for activity_id in activity_ids:
            try:
                count += 1
                detailed_activity = self.api.get_activity(id=activity_id)
                self.db.insert_activity(detailed_activity,"strava_bronze.activities_detailed")
                logger.info(
                        "Activity loaded",
                        extra={"activity_id": activity_id, "progress": f"{count}/{len(activity_ids)}"}
                    )
            except Exception as e:
               logger.error("Failed to load activity", extra={"activity_id": activity_id, "error": str(e)})
               
            time.sleep(40)


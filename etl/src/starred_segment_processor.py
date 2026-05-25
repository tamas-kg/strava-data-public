from src.postgres_db import PostgresDB
from src.logger import setup_logger

class StarredSegmentProcessor:
    def __init__(self, db: PostgresDB):
        self.db = db
    
    def process_starred_segments(self, segments:dict) -> None:
        """Process and insert starred segments into the database."""
        for segment in segments:
            self.db.insert_starred_segment(segment)

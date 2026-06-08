from app.repositories.segments_repository import SegmentsRepository
from app.services.cache_service import CacheService


class SegmentsService:

    def __init__(self):
        self.repo = SegmentsRepository()
        self.cache = CacheService()

    def get_efforts(self):
    
        if cached := self.cache.get("efforts"):
            return cached

        data = self.repo.get_efforts()

        self.cache.set(
            "efforts",
            data,
            ttl=300
        )

        return data
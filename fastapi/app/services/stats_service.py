from app.repositories.stats_repository import StatsRepository
from app.services.cache_service import CacheService


class StatsService:

    def __init__(self):
        self.repo = StatsRepository()
        self.cache = CacheService()

    def get_monthly_stats(self):
        if cached := self.cache.get("monthly_stats"):
            return cached

        data = self.repo.get_monthly_stats()

        self.cache.set(
            "monthly_stats",
            data,
            ttl=300
        )

        return data
from app.repositories.routes_repository import RoutesRepository
from app.services.cache_service import CacheService


class RoutesService:

    def __init__(self):
        self.repo = RoutesRepository()
        self.cache = CacheService()

    def get_routes(self):
    
        if cached := self.cache.get("routes"):
            return cached

        data = self.repo.get_routes()

        self.cache.set(
            "routes",
            data,
            ttl=300
        )

        return data
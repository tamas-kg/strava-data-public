import json
from app.core.redis import redis_client


class CacheService:

    def get(self, key: str) -> dict:
        """ Try to get query results from redis cache """
        data = redis_client.get(key)

        if data:
            return json.loads(data)

        return None

    def set(self, key: str, value, ttl: int = 300) -> None:
        """ Add query results to redis cache for future queries """
        redis_client.setex(
            key,
            ttl,
            json.dumps(value, default=str)
        )

    def delete(self, key: str):
        """ Delete cached results """
        redis_client.delete(key)
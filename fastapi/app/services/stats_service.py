from app.repositories.stats_repository import StatsRepository


class StatsService:

    def __init__(self):
        self.repo = StatsRepository()

    def get_monthly_stats(self):
        return self.repo.get_monthly_stats()
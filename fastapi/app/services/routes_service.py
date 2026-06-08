from app.repositories.routes_repository import RoutesRepository


class RoutesService:

    def __init__(self):
        self.repo = RoutesRepository()

    def get_routes(self):
        return self.repo.get_routes()
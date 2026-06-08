from app.repositories.segments_repository import SegmentsRepository


class SegmentsService:

    def __init__(self):
        self.repo = SegmentsRepository()

    def get_efforts(self):
        return self.repo.get_efforts()
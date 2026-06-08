from fastapi import APIRouter
from app.services.stats_service import StatsService
from app.models.schemas import MonthlyStat

router = APIRouter()

service = StatsService()

@router.get(
    "/monthly",
    response_model=list[MonthlyStat]
)
def get_monthly_stats():
    return service.get_monthly_stats()
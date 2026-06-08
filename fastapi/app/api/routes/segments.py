from fastapi import APIRouter
from app.services.segments_service import SegmentsService
from app.models.schemas import Effort

router = APIRouter()

service = SegmentsService()

@router.get(
    "/efforts",
    response_model=list[Effort]
)
def get_efforts():
    return service.get_efforts()
from fastapi import APIRouter
from app.services.routes_service import RoutesService
from app.models.schemas import Route

router = APIRouter()

service = RoutesService()

@router.get(
    "/routes",
    response_model=list[Route]
)
def get_map_data():
    return service.get_routes()
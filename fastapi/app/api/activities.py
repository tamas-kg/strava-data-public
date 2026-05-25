from fastapi import APIRouter

router = APIRouter(prefix="/activities")

@router.get("/")
async def activities():
    return [
        {
            "id": 1,
            "name": "Morning Ride"
        }
    ]
from fastapi import FastAPI
from app.api.activities import router as activities_router

app = FastAPI()

app.include_router(activities_router)

@app.get("/health")
async def health():
    return {"status": "ok"}
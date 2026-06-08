from fastapi import FastAPI
from app.api.routes import stats, routes, segments

app = FastAPI()


app.include_router(
    stats.router,
    prefix="/stats",
    tags=["stats"]
)

app.include_router(
    routes.router,
    tags=["routes"]
)

app.include_router(
    segments.router,
    prefix="/segments",
    tags=["segments"]
)

@app.get("/health")
async def health():
    return {"status": "ok"}
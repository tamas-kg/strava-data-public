from pydantic import BaseModel
from datetime import timedelta, datetime

class MonthlyStat(BaseModel):
    year: int
    month: int
    year_month: str
    month_name: str
    month_num: int
    total_distance: float
    total_time: timedelta
    total_elevation: float
    total_calories: float
    total_prs: int

class Route(BaseModel):
    geojson_geom: str
    route_geom: str

class Effort(BaseModel):
    segment_id: int
    name: str
    start_date: datetime
    elapsed_time: timedelta
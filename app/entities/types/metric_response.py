
from typing import List
from pydantic import BaseModel
from app.entities.models.events import Events
from app.entities.models.product import ProductPopularity

class MetricResponse(BaseModel):
    total_revenue: float
    purchases: int
    unique_users: int
    conversion_rate: float
    top_products: List[ProductPopularity]


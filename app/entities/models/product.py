from pydantic import BaseModel


class ProductPopularity(BaseModel):
    product_id: str
    price: float
    purchases: int
    views: int
    revenue: float

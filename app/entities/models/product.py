from pydantic import BaseModel, Field


class ProductPopularity(BaseModel):
    product_id: str
    price: float = Field(ge=0.00)
    purchases: int = Field(ge=0)
    views: int = Field(ge=0)
    revenue: float = Field(ge=0.00)

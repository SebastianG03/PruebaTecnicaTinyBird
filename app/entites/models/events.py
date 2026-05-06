from datetime import datetime

from sqlmodel import SQLModel, Field

class Events(SQLModel, table=True):
    event_id: str = Field(primary_key=True, index=True, unique=True)
    user_id: str = Field(index=True, include="u_", regex="u_[0-9]+")
    event_type: str = Field(regex="product_view|add_to_cart|purchase")
    product_id: str = Field(index=True, include="p_", regex="p_[0-9]+")
    timestamp: datetime
    price: float = Field(decimal_places=2, ge=0)
    country: str = Field(min_length=2, max_length=2)

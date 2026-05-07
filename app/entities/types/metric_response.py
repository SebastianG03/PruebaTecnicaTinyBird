
from typing import List

from pydantic import BaseModel

from app.entities.models.events import Events

class MetricResponse(BaseModel):
    total_events: int
    events: List[Events]
    errors: List[str]
    invalid_events: int
    duplicated_events: int

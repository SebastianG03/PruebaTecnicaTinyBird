
from datetime import datetime
from email import message
from typing import List, Optional, Union

from fastapi_cache.decorator import cache
from fastapi import APIRouter

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.utils import load_events
from app.core.validate_events import EventValidator
from app.entities.models.events import Events
from app.entities.models.get_metrics import MetricsEntry
from app.entities.models.web_response import WebResponse
from app.entities.types.response_type import TypeResponses

limiter = Limiter(key_func=get_remote_address)

metrics_router = APIRouter(
    prefix="/metrics",
    tags=["metrics"]
)

@metrics_router.get("/")
@cache(expire=60)
@limiter.limit("500/minute")
async def get_metrics(metrics_entry: MetricsEntry):
    events = load_events()

    event_validator = EventValidator()
    response = event_validator.total_events(events, metrics_entry)

    return WebResponse.response(
        type=TypeResponses.SUCCESS,
        title="Métricas",
        messsage="Métricas obtenidas conéxito",
        content=response.model_dump_json(),
        http_code=200
    )

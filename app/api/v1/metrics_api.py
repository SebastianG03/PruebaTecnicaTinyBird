from pathlib import Path
import traceback

from fastapi_cache.decorator import cache
from fastapi import APIRouter

import logfire

from app.core.metrics_manager import MetricsManager
from app.core.utils import load_events
from app.core.validate_events import EventValidator
from app.entities.models.get_metrics import MetricsEntry
from app.entities.models.web_response import WebResponse
from app.entities.types.response_type import TypeResponses

metrics_router = APIRouter(prefix="/metrics", tags=["metrics"])


@metrics_router.get("/health")
def health():
    return {"status": "ok"}


@metrics_router.post("/", status_code=200)
@cache(expire=60)
async def get_metrics(metrics_entry: MetricsEntry):
    try:
        events = load_events(Path("./data/events.json"))

        event_validator = EventValidator()
        events = event_validator.total_events(events, metrics_entry)
        metrics = MetricsManager().calculate_metrics(events)

        return WebResponse.response(
            type=TypeResponses.SUCCESS,
            title="Métricas",
            messsage="Métricas obtenidas con éxito",
            content=metrics.model_dump(),
            http_code=200,
        )
    except ValueError as e:
        logfire.error(traceback.format_exc())
        return WebResponse.response(
            type=TypeResponses.ERROR,
            title="Error",
            messsage=str(e),
            content=None,
            http_code=400,
        )
    except FileNotFoundError as de:
        logfire.error(traceback.format_exc())
        return WebResponse.response(
            type=TypeResponses.ERROR,
            title="Error",
            messsage=str(de),
            content=None,
            http_code=400,
        )
    except Exception as e:
        logfire.error(traceback.format_exc())
        return WebResponse.response(
            type=TypeResponses.ERROR,
            title="Error",
            messsage=str(e),
            content=None,
            http_code=500,
        )

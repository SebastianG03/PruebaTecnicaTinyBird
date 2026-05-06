
from datetime import datetime
from typing import List, Optional, Union

from fastapi_cache.decorator import cache
from fastapi import APIRouter

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.entites.models.events import Events

limiter = Limiter(key_func=get_remote_address)

metrics_router = APIRouter(
    prefix="/metrics",
    tags=["metrics"]
)

@metrics_router.get("/")
@cache(expire=60)
@limiter.limit("500/minute")
async def get_metrics(
    contry: Optional[str] = None,
    from_date: Optional[datetime] = None,
    to_date: Optional[datetime] = None):
    pass
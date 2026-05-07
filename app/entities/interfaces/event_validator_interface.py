from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union

from app.entities.models.events import Events
from app.entities.interfaces.singleton import Singleton
from app.entities.models.get_metrics import MetricsEntry
from app.entities.types.metric_response import MetricResponse


class IEventValidator(Singleton, ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def total_events(self, events: List[Dict], metrics_entry: MetricsEntry) -> MetricResponse:
        pass

    @abstractmethod
    def valid_events(self, events: List[Dict]) -> Tuple[List[Events], List[str], int]:
        "Devuelve una lista de los eventos válidos, una lista de los errores encontrados y el total de eventos inválidos"
        pass

    @abstractmethod
    def duplicated_events(self, events: List[Dict]):
        registered_events = set()
        duplicated = 0
        for event in events:
            event_id = event.get('event_id', "")

            if event_id == "":
                continue

            if event_id in registered_events: 
                duplicated += 1
            else:
                registered_events.add(event_id)

        return duplicated

    def filter_events_by_country(self, events: List[Events], country_code: str):
        country_code = country_code.upper().strip()
        return [event for event in events if event.country.upper().strip() == country_code]

    def filter_events_by_dates(self, events: List[Events], start_date: Optional[datetime], end_date: Optional[datetime]):
        if start_date and end_date:
            return [
                event for event in events
                if datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") >= start_date and
                datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") <= end_date]

        if start_date:
            return [
                event for event in events
                if datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") >= start_date]

        if end_date:
            return [
                event for event in events
                if datetime.strptime(event.timestamp, "%Y-%m-%dT%H:%M:%SZ") <= end_date]

        return events
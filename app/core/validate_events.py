import traceback
from typing import Dict, List, Optional, Union

from app.entities.interfaces.event_validator_interface import IEventValidator
from app.entities.interfaces.singleton import Singleton
from app.entities.models.events import Events

import logfire

from app.entities.models.get_metrics import MetricsEntry
from app.entities.types.metric_response import MetricResponse

class EventValidator(IEventValidator):
    def __init__(self):
        pass

    def total_events(self, events: List[Dict], metrics_entry: MetricsEntry):
        collected_events, error_collector, invalid_count = self.valid_events(events)
        events_dict = [collected_event.model_dump() for collected_event in collected_events]

        duplicated = self.duplicated_events(events_dict)

        country, from_date, to_date = metrics_entry.country, metrics_entry.from_date, metrics_entry.to_date

        if country:
            collected_events = self.filter_events_by_country(collected_events, country)

        collected_events = self.filter_events_by_dates(collected_events, from_date, to_date)
        total = len(events)

        return MetricResponse(
            total_events=total,
            events=collected_events,
            errors=error_collector,
            invalid_events=invalid_count,
            duplicated_events=duplicated)

    
    def valid_events(self, events: List[Dict]):
        collected_events: List[Events] = []
        error_collector: List[str] = []
        invalid_count = 0
        for event in events:
            try:
                ev = Events.model_validate(**event)
                collected_events.append(ev)
            except ValueError:
                error = traceback.format_exc()
                logfire.error(error)
                error_collector.append(error)
                invalid_count += 1
                continue

        return collected_events, error_collector, invalid_count
    
    def duplicated_events(self, events: List[Dict]):
        return super().duplicated_events(events)
    
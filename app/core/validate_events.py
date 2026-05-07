from datetime import datetime
import traceback
from typing import Dict, List

from app.entities.interfaces.event_validator_interface import IEventValidator
from app.entities.models.events import Events

import logfire

from app.entities.models.get_metrics import MetricsEntry


class EventValidator(IEventValidator):
    def __init__(self):
        pass

    def total_events(self, events: List[Dict], metrics_entry: MetricsEntry):
        collected_events, error_collector, invalid_count = self.valid_events(events)
        collected_events, duplicated = self.duplicated_events(collected_events)

        country, from_date, to_date = (
            metrics_entry.country,
            metrics_entry.from_date,
            metrics_entry.to_date,
        )

        if country is not None and country != "":
            collected_events = self.filter_events_by_country(collected_events, country)

        try:
            from_date = (
                datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%SZ")
                if from_date
                else None
            )
            to_date = (
                datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%SZ") if to_date else None
            )
        except Exception:
            logfire.error(traceback.format_exc())
            from_date, to_date = None, None

        collected_events = self.filter_events_by_dates(
            collected_events, from_date, to_date
        )
        total = len(events)
        logfire.info(
            f"Total events: {total}, duplicated events: {duplicated}, invalid events: {invalid_count}, errors: {len(error_collector)}"
        )
        logfire.info(f"Errors found on processing events: {error_collector}")

        return collected_events

    def valid_events(self, events: List[Dict]):
        collected_events: List[Events] = []
        error_collector: List[str] = []
        invalid_count = 0
        for event in events:
            try:
                ev = Events.model_validate(event)
                collected_events.append(ev)
            except ValueError:
                error = traceback.format_exc()
                logfire.error(error)
                error_collector.append(error)
                invalid_count += 1
                continue

        return collected_events, error_collector, invalid_count

    def duplicated_events(self, events: List[Events]):
        return super().duplicated_events(events)

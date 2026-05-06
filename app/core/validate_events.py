from typing import List, Union

from app.entites.interfaces.event_validator_interface import IEventValidator
from app.entites.interfaces.singleton import Singleton
from app.entites.models.events import Events


class EventValidator(IEventValidator):
    def __init__(self):
        pass

    def total_events(self, events: Union[Events, List[Events]]):
        return super().total_events(events)
    
    def valid_events(self, events: Union[Events, List[Events]]):
        return super().valid_events(events)
    
    def invalid_events(self, events: Union[Events, List[Events]]):
        return super().invalid_events(events)
    
    def duplicated_events(self, events: Union[Events, List[Events]]):
        return super().duplicated_events(events)

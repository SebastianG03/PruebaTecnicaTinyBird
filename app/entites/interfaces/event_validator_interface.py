from abc import ABCMeta, abstractmethod
from typing import List, Union

from app.entites.models.events import Events
from app.entites.interfaces.singleton import Singleton


class IEventValidator(Singleton, ABCMeta):
    @abstractmethod
    def total_events(self, events: Union[Events, List[Events]]):
        pass

    @abstractmethod
    def valid_events(self, events: Union[Events, List[Events]]):
        pass

    @abstractmethod
    def invalid_events(self, events: Union[Events, List[Events]]):
        pass

    @abstractmethod
    def duplicated_events(self, events: Union[Events, List[Events]]):
        pass

from abc import ABCMeta, abstractmethod
from typing import List, Union

from app.entities.models.events import Events
from app.entities.interfaces.singleton import Singleton


class IMetrics(Singleton, ABCMeta):

    @abstractmethod
    def total_revenue(self):
        pass
    @abstractmethod
    def purchases(self):
        pass
    @abstractmethod
    def unique_users(self):
        pass
    @abstractmethod
    def conversion_rate(self):
        pass
    @abstractmethod
    def top_products(self):
        pass

    def _calculate_conversion_rate(self, number_users: int, number_products_viewed: int) -> float:
        return number_users / number_products_viewed

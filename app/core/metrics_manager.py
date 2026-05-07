from decimal import Decimal
from typing import Dict, List
from app.entities.interfaces.singleton import Singleton
from app.entities.models.events import Events
from app.entities.models.product import ProductPopularity
from app.entities.types.event_type import EventTypes
from app.entities.types.metric_response import MetricResponse


class MetricsManager(metaclass=Singleton):
    def group_by_event_type(self, events: List[Events]):
        grouped_events = {}

        for event in events:
            event_type = event.event_type
            if event_type not in grouped_events:
                grouped_events[event_type] = []
            grouped_events[event_type].append(event)

        return grouped_events
    

    def calculate_metrics(self, events: List[Events]):
        if not events or len(events) == 0:
            return MetricResponse(
                total_revenue=0,
                purchases=0,
                unique_users=0,
                conversion_rate=0,
                top_products=[]
            )

        grouped_events = self.group_by_event_type(events)

        purchases = 0
        total_revenue = 0
        users_who_purchased = set()
        users_who_viewed = set()
        dict_products: Dict[str, ProductPopularity] = {}

        for event_type, events in grouped_events.items():
            if event_type == EventTypes.PURCHASE:
                for event in events:
                    total_revenue += float(event.price)
                    if event.user_id:
                        users_who_purchased.add(event.user_id)
                    
                    if event.product_id not in dict_products:
                        dict_products[event.product_id] = ProductPopularity(
                            product_id=event.product_id,
                            price=float(event.price),
                            purchases=1,
                            views=0,
                            revenue=float(event.price)
                        )
                    else:
                        dict_products[event.product_id].purchases += 1
                        dict_products[event.product_id].revenue += float(event.price)

                    purchases += 1
            elif event_type == EventTypes.PRODUCT_VIEW:
                for event in events:
                    if event.user_id:
                        users_who_viewed.add(event.user_id)
                    
                    if event.product_id not in dict_products:
                        dict_products[event.product_id] = ProductPopularity(
                            product_id=event.product_id,
                            price=float(event.price),
                            purchases=0,
                            views=1,
                            revenue=0
                        )
                    else:
                        dict_products[event.product_id].views += 1

        conversion_rate = self._calculate_conversion_rate(len(users_who_purchased), len(users_who_viewed))
        unique_users = users_who_purchased.union(users_who_viewed)

        top_products = [product for product in dict_products.values()]
        top_products.sort(key=lambda x: x.purchases, reverse=True)

        return MetricResponse(
            total_revenue=total_revenue,
            conversion_rate=conversion_rate,
            purchases=purchases,
            unique_users=len(unique_users),
            top_products=top_products
        )


    def _calculate_conversion_rate(self, number_users: int, number_products_viewed: int) -> float:
        if number_products_viewed == 0 or number_users == 0:
            return 0

        return number_users / number_products_viewed

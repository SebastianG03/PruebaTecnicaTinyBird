from enum import StrEnum


class EventTypes(StrEnum):
    PURCHASE = "purchase"
    PRODUCT_VIEW = "product_view"
    ADD_TO_CART = "add_to_cart"

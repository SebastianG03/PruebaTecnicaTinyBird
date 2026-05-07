import pytest
from app.entities.models.events import Events
from app.entities.types.event_type import EventTypes


@pytest.fixture
def valid_event_data():
    return {
        "event_id": "evt_001234",
        "user_id": "u_123456",
        "event_type": EventTypes.PRODUCT_VIEW,
        "product_id": "p_101",
        "timestamp": "2025-05-03T10:15:00Z",
        "price": 99.99,
        "country": "EC",
    }


def test_events_model_valid(valid_event_data):
    """Comprueba la validación del modelo de eventos"""
    event = Events.model_validate(valid_event_data)
    assert event.event_id == "evt_001234"
    assert event.user_id == "u_123456"
    assert event.event_type == EventTypes.PRODUCT_VIEW
    assert event.price == 99.99
    assert event.country == "EC"


def test_events_invalid_fields():
    """Comprueba la validación de campos de eventos inválidos"""
    data = {
        "event_id": "evt_001234",
        "user_id": "u_123456",
        "event_type": EventTypes.PRODUCT_VIEW,
        "product_id": "p_101",
        "timestamp": "2025-05-03T10:15:00Z",
        "price": -10,
        "country": "EC",
    }

    with pytest.raises(ValueError) as exc_info:
        Events.model_validate(data)
    assert len(str(exc_info.value)) > 0


def test_purchase_with_zero_price_invalid():
    data = {
        "event_id": "evt_001",
        "user_id": "u_123",
        "event_type": EventTypes.PURCHASE,
        "product_id": "p_10",
        "timestamp": "2025-05-03T10:15:00Z",
        "price": 0,
        "country": "CR",
    }
    with pytest.raises(ValueError) as exc_info:
        Events.model_validate(data)
    assert "El precio no puede ser 0 para un evento de compra" in str(exc_info.value)


def test_event_type_invalid():
    data = {
        "event_id": "evt_001",
        "user_id": "u_123",
        "event_type": "invalid_event",
        "product_id": "p_10",
        "timestamp": "2025-05-03T10:15:00Z",
        "price": 50,
        "country": "EC",
    }
    with pytest.raises(ValueError) as exc_info:
        Events.model_validate(data)
    assert "El tipo de evento no es válido" in str(exc_info.value)


def test_timestamp_various_formats():
    """Prueba diferentes formatos de timestamp válidos"""
    formats = [
        "2025-05-03T10:15:00",
        "2025-05-03T10:15:00Z",
        "2025-05-03T10:15:00+00:00",
    ]
    for ts in formats:
        data = {
            "event_id": "evt_001234",
            "user_id": "u_123456",
            "event_type": EventTypes.PRODUCT_VIEW,
            "product_id": "p_101",
            "timestamp": ts,
            "price": 10.0,
            "country": "EC",
        }
        event = Events.model_validate(data)
        assert event.timestamp == ts

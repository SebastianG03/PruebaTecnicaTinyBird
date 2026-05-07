import pytest
import json
from pathlib import Path

from app.entities.models.events import Events
from app.core.validate_events import EventValidator
from app.entities.models.get_metrics import MetricsEntry
from app.entities.types.event_type import EventTypes
from app.entities.types.metric_response import MetricResponse
from app.core.metrics_manager import MetricsManager


@pytest.fixture(scope="module")
def raw_test_events():
    """Carga el archivo JSON completo"""
    file_path = Path("./data/test_events.json")

    return json.loads(file_path.read_text())


@pytest.fixture(scope="module")
def valid_events(raw_test_events):
    """Retorna solo los eventos que pasan la validación"""
    validator = EventValidator()
    events = validator.total_events(
        raw_test_events, MetricsEntry(country="", from_date="", to_date="")
    )
    return events


@pytest.fixture
def metrics_manager():
    return MetricsManager()


def test_calculate_metrics_empty_list(metrics_manager):
    """Prueba sin eventos"""
    result = metrics_manager.calculate_metrics([])

    assert isinstance(result, MetricResponse)
    assert result.total_revenue == 0
    assert result.purchases == 0
    assert result.unique_users == 0
    assert result.conversion_rate == 0
    assert result.top_products == []


def test_calculate_metrics_with_valid_events(valid_events, metrics_manager):
    """Prueba principal con datos de prueba"""
    result = metrics_manager.calculate_metrics(valid_events)

    assert isinstance(result, MetricResponse)
    assert result.total_revenue > 0
    assert result.purchases > 0
    assert result.unique_users > 0
    assert 0 <= result.conversion_rate <= 1
    assert len(result.top_products) > 0


def test_group_by_event_type(valid_events, metrics_manager):
    """Valida que el agrupamiento se realice en almenos uno de los tipos de eventos existentes"""
    grouped = metrics_manager.group_by_event_type(valid_events)
    event_types = [event_type.value for event_type in EventTypes]

    assert isinstance(grouped, dict)
    assert set(grouped.keys()).issubset(event_types)
    assert (
        "product_view" in grouped or "add_to_cart" in grouped or "purchase" in grouped
    )


def test_revenue_calculation(valid_events, metrics_manager):
    """Verifica que el revenue se calcule correctamente"""
    result = metrics_manager.calculate_metrics(valid_events)

    expected_revenue = sum(
        float(e.price) for e in valid_events if e.event_type == "purchase"
    )

    assert abs(result.total_revenue - expected_revenue) < 0.01


def test_top_products_ranking(valid_events, metrics_manager):
    """Verifica que los productos estén ordenados por compras descendente"""
    result = metrics_manager.calculate_metrics(valid_events)

    top_products = result.top_products
    assert len(top_products) > 0

    for i in range(len(top_products) - 1):
        assert top_products[i].purchases >= top_products[i + 1].purchases


def test_conversion_rate(valid_events, metrics_manager):
    """Prueba la tasa de conversión"""
    result = metrics_manager.calculate_metrics(valid_events)

    assert isinstance(result.conversion_rate, float)
    assert 0 <= result.conversion_rate <= 1.0


def test_unique_users_count(valid_events, metrics_manager):
    """Verifica conteo de usuarios únicos"""
    result = metrics_manager.calculate_metrics(valid_events)

    unique_users_from_events = len({e.user_id for e in valid_events if e.user_id})

    assert result.unique_users <= unique_users_from_events


@pytest.fixture
def generate_test_events():
    """Eventos de prueba para el testeo de cálculos"""
    return [
        Events.model_validate(
            {
                "event_id": "evt_001",
                "user_id": "u_123",
                "event_type": "product_view",
                "product_id": "p_10",
                "timestamp": "2025-05-03T10:15:00Z",
                "price": 0,
                "country": "CR",
            }
        ),
        Events.model_validate(
            {
                "event_id": "evt_002",
                "user_id": "u_123",
                "event_type": "product_view",
                "product_id": "p_10",
                "timestamp": "2025-05-03T10:16:00Z",
                "price": 0,
                "country": "CR",
            }
        ),
        Events.model_validate(
            {
                "event_id": "evt_003",
                "user_id": "u_456",
                "event_type": "purchase",
                "product_id": "p_10",
                "timestamp": "2025-05-03T10:20:00Z",
                "price": 99.99,
                "country": "CR",
            }
        ),
        Events.model_validate(
            {
                "event_id": "evt_004",
                "user_id": "u_789",
                "event_type": "purchase",
                "product_id": "p_25",
                "timestamp": "2025-05-04T10:00:00Z",
                "price": 149.50,
                "country": "EC",
            }
        ),
    ]


def test_metrics_with_controlled_data(generate_test_events, metrics_manager):
    result = metrics_manager.calculate_metrics(generate_test_events)

    assert result.purchases == 2
    assert result.total_revenue == 99.99 + 149.50
    assert result.unique_users == 3
    assert len(result.top_products) == 2

    top_products = next(p for p in result.top_products if p.product_id == "p_10")
    assert top_products.purchases == 1
    assert top_products.views == 2

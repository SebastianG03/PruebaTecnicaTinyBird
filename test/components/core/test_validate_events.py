import pytest
import json
from pathlib import Path
from datetime import datetime

from app.core.validate_events import EventValidator
from app.entities.models.get_metrics import MetricsEntry


@pytest.fixture(scope="module")
def test_events():
    """Carga el archivo con los eventos para pruebas"""
    file_path = Path("./data/test_events.json")
    return json.loads(file_path.read_text())


@pytest.fixture
def validator():
    return EventValidator()


def test_load_test_file(test_events):
    """Verifica que el archivo se encuentre disponible y tenga contenido para las pruebas"""
    assert isinstance(test_events, list)
    assert len(test_events) > 40


def test_valid_events_count(test_events, validator):
    """Prueba cuántos eventos son válidos según el modelo Events"""
    valid_events, errors, invalid_count = validator.valid_events(test_events)

    print(f"\nEventos totales: {len(test_events)}")
    print(f"Eventos válidos: {len(valid_events)}")
    print(f"Eventos inválidos: {invalid_count}")
    print(f"Errores capturados: {len(errors)}")

    assert len(valid_events) > 30
    assert invalid_count >= 3


def test_duplicated_events(test_events, validator):
    """Prueba la eliminación de duplicados"""
    valid_events, _, _ = validator.valid_events(test_events)
    deduplicated, duplicated_count = validator.duplicated_events(valid_events)

    assert duplicated_count > 3
    assert len(deduplicated) < len(valid_events)


def test_filter_by_country(test_events, validator):
    """Filtrado por país"""
    valid_events, _, _ = validator.valid_events(test_events)

    ec_events = validator.filter_events_by_country(valid_events, "EC")
    cr_events = validator.filter_events_by_country(valid_events, "CR")

    assert len(ec_events) > 3
    assert all(event.country == "EC" for event in ec_events)
    assert len(cr_events) >= 8


def test_filter_by_date_range(test_events, validator):
    """Filtrado por rango de fechas"""
    valid_events, _, _ = validator.valid_events(test_events)

    from_date = datetime(2024, 1, 1)
    to_date = datetime(2025, 12, 31)

    filtered = validator.filter_events_by_dates(valid_events, from_date, to_date)

    assert len(filtered) > 10

    for event in filtered[:5]:
        event_date = datetime.fromisoformat(event.timestamp.replace("Z", "+00:00"))
        event_date = event_date.replace(tzinfo=None)

        assert from_date <= event_date <= to_date


def test_total_events_full_flow(test_events, validator):
    """Prueba completa del método principal"""
    metrics_entry = MetricsEntry(
        from_date="2023-01-01T00:00:00Z", to_date="2025-12-31T23:59:59Z", country="CR"
    )

    result = validator.total_events(test_events, metrics_entry)

    assert isinstance(result, list)
    assert len(result) > 2

    if result:
        assert all(e.country == "CR" for e in result)


def test_total_events_filter_only_date(test_events, validator):
    """Filtra sólo por rango de fechas"""
    metrics_entry = MetricsEntry(
        from_date="2022-01-01T00:00:00Z", to_date="2025-12-31T23:59:59Z", country=""
    )

    result = validator.total_events(test_events, metrics_entry)
    assert len(result) > 20


def test_error_detection(test_events, validator):
    """Prueba casos específicos inválidos que deberían ser detectados"""
    _, errors, invalid_count = validator.valid_events(test_events)

    assert len(errors) > 5
    assert invalid_count > 5

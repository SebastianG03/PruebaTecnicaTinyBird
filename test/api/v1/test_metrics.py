from pathlib import Path

import pytest
import json
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app

client = TestClient(app)


@pytest.fixture
def mock_events():
    file = Path("./data/test_events.json")
    return json.loads(file.read_text())

@pytest.fixture
def metrics_request():
    return {
                "country": "CR",
                "from_date": "2022-01-01T00:00:00Z",
                "to_date": "2025-12-31T00:00:00Z"
            }

def test_health_endpoint():
    """Prueba el endpoint de health"""
    response = client.get("/metrics/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_metrics_success(mock_events, metrics_request):
    """Prueba con datos correctos filtrando por fecha y país"""
    
    with patch('app.core.utils.load_events') as mock_load:
        mock_load.return_value = mock_events
        
        response = client.post(
            "/metrics/",
            json=metrics_request
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["type"].upper() == "SUCCESS"
        assert data["title"] == "Métricas"
        assert "data" in data
        assert isinstance(data["data"], dict)


def test_get_metrics_invalid_dates():
    """Prueba con fechas inválidas (debería fallar en el validador)"""
    payload = {
        "from_date": "2025-01-01T00:00:00Z",
        "to_date": "2022-01-01T00:00:00Z"
    }
    
    response = client.post("/metrics/", json=payload)
    assert response.status_code == 400

def test_invalid_country():
    """Prueba con países inválido, falla al validar"""
    payload = {
        "country": "XX",
        "from_date": "2022-01-01T00:00:00Z",
        "to_date": "2025-12-31T00:00:00Z"
    }
    
    response = client.post("/metrics/", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "El código de país no es válido"

def test_metrics_without_dates():
    """Prueba sin fechas, devuelve unicamente filtrado por pais"""
    payload = {
        "country": "EC",
        "from_date": "",
        "to_date": ""
        }
    
    response = client.post("/metrics/", json=payload)
    assert response.status_code == 200
    assert response.json()["type"].upper() == "SUCCESS"
    assert response.json()["data"] != {}

def test_get_metrics_missing_fields():
    """Prueba con campos obligatorios faltantes"""
    response = client.post("/metrics/", json={})
    assert response.status_code == 422


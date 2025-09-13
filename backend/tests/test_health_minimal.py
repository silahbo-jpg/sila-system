"""Minimal test file to verify test execution."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data

def test_health_metrics():
    """Test the health metrics endpoint."""
    response = client.get("/health/metrics")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_health_api_endpoints():
    """Test the health API endpoints."""
    # Test GET /health/
    response = client.get("/health/")
    assert response.status_code == 200
    
    # Test GET /health/metrics
    response = client.get("/health/metrics")
    assert response.status_code == 200
    
    # Test POST /health/ (should be 405 Method Not Allowed)
    test_data = {
        "tipo_consulta": "Teste de integração",
        "data_consulta": "2025-08-16T10:00:00",
        "diagnostico": "Teste",
        "tratamento": "Nenhum",
        "observacoes": "Teste de integração",
        "cidadao_id": "00000000-0000-0000-0000-000000000000"
    }
    response = client.post("/health/", json=test_data)
    assert response.status_code == 405  # Method Not Allowed


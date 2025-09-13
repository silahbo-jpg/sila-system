from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_relatorio_mensal():
    resp = client.get("/api/statistics/relatorio-mensal")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for item in data:
        assert "mes" in item
        assert "total_atestados" in item
        assert "total_licencas" in item
        assert "total_certidoes" in item


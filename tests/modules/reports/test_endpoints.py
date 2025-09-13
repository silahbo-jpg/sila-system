from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_consultar_relatorios_todos():
    resp = client.post("/api/reports/filtrar", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    for item in data:
        assert "tipo" in item
        assert "nome_requerente" in item
        assert "data_emissao" in item
        assert "descricao" in item

def test_consultar_relatorios_filtrado():
    payload = {"tipo": "licencas"}
    resp = client.post("/api/reports/filtrar", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    for item in data:
        assert item["tipo"] == "Licença Comercial"


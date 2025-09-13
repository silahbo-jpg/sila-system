from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_atestado():
    payload = {
        "nome_completo": "João Manuel",
        "numero_bi": "123456789LA034",
        "morada": "Maianga, Luanda",
        "finalidade": "Abertura de conta bancária"
    }
    response = client.post("/api/citizenship/atestado/", json=payload)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["nome_completo"] == payload["nome_completo"]
    assert data["numero_bi"] == payload["numero_bi"]
    assert data["morada"] == payload["morada"]
    assert data["finalidade"] == payload["finalidade"]
    assert data["estado"] == "pendente"
    assert "id" in data
    assert "criado_em" in data

def test_get_atestado():
    # Primeiro cria
    payload = {
        "nome_completo": "Carlos Silva",
        "numero_bi": "987654321LA098",
        "morada": "Kilamba, Luanda",
        "finalidade": "Processo escolar"
    }
    post_resp = client.post("/api/citizenship/atestado/", json=payload)
    atestado_id = post_resp.json()["id"]
    # Busca
    get_resp = client.get(f"/api/citizenship/atestado/{atestado_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == atestado_id
    assert data["nome_completo"] == payload["nome_completo"]

def test_pdf_endpoint():
    payload = {
        "nome_completo": "Ana Paula",
        "numero_bi": "111222333LA000",
        "morada": "Benfica, Luanda",
        "finalidade": "Comprovação de residência"
    }
    post_resp = client.post("/api/citizenship/atestado/", json=payload)
    atestado_id = post_resp.json()["id"]
    pdf_resp = client.get(f"/api/citizenship/atestado/{atestado_id}/pdf")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"].startswith("application/pdf")


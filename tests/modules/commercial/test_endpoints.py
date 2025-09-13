from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_licenca():
    payload = {
        "nome_empresa": "Comercial XYZ",
        "nif": "500100200",
        "atividade": "Restaurante",
        "endereco": "Rua do Comércio, Luanda",
        "validade": "2025-12-31"
    }
    headers = {"Authorization": "Bearer admin-token"}
    response = client.post("/api/commercial/licenca/", json=payload, headers=headers)
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["nome_empresa"] == payload["nome_empresa"]
    assert data["nif"] == payload["nif"]
    assert data["atividade"] == payload["atividade"]
    assert data["endereco"] == payload["endereco"]
    assert data["validade"] == payload["validade"]
    assert data["estado"] == "pendente"
    assert "id" in data
    assert "criado_em" in data

def test_get_licenca():
    payload = {
        "nome_empresa": "Empresa ABC",
        "nif": "123456789",
        "atividade": "Consultoria",
        "endereco": "Avenida Central, Luanda",
        "validade": "2026-01-01"
    }
    headers = {"Authorization": "Bearer admin-token"}
    post_resp = client.post("/api/commercial/licenca/", json=payload, headers=headers)
    licenca_id = post_resp.json()["id"]
    get_resp = client.get(f"/api/commercial/licenca/{licenca_id}", headers=headers)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["id"] == licenca_id
    assert data["nome_empresa"] == payload["nome_empresa"]

def test_get_licenca_inexistente():
    headers = {"Authorization": "Bearer admin-token"}
    resp = client.get("/api/commercial/licenca/99999", headers=headers)
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Licença não encontrada"

def test_create_licenca_invalida():
    headers = {"Authorization": "Bearer admin-token"}
    # Falta campo obrigatório
    payload = {"nome_empresa": "Invalida"}
    resp = client.post("/api/commercial/licenca/", json=payload, headers=headers)
    assert resp.status_code == 422

def test_pdf_endpoint():
    payload = {
        "nome_empresa": "Loja Nova",
        "nif": "987654321",
        "atividade": "Varejo",
        "endereco": "Mercado Municipal, Luanda",
        "validade": "2027-03-15"
    }
    headers = {"Authorization": "Bearer admin-token"}
    post_resp = client.post("/api/commercial/licenca/", json=payload, headers=headers)
    licenca_id = post_resp.json()["id"]
    pdf_resp = client.get(f"/api/commercial/licenca/{licenca_id}/pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"].startswith("application/pdf")


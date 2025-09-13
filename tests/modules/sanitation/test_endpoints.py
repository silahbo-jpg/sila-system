from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_certidao():
    payload = {
        "titular": "Maria Silva",
        "local_atividade": "Açougue Central",
        "finalidade": "Funcionamento"
    }
    resp = client.post("/api/sanitation/", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["titular"] == payload["titular"]
    assert data["local_atividade"] == payload["local_atividade"]
    assert data["finalidade"] == payload["finalidade"]
    assert "id" in data
    assert "emitido_em" in data

    # Testa PDF
    certidao_id = data["id"]
    pdf_resp = client.get(f"/api/sanitation/{certidao_id}/pdf")
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"

def test_certidao_inexistente():
    resp = client.get("/api/sanitation/99999/pdf")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Certidão não encontrada"


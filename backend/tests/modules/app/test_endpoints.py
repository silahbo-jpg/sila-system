import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.justice.schemas import JudicialCertificateCreate

client = TestClient(app)

def test_issue_certificate_endpoint(monkeypatch):
    def fake_generate_pdf(filename, data):
        return "/tmp/certificate_1.pdf"
    monkeypatch.setattr("app.utils.pdf_generator.generate_pdf", fake_generate_pdf)
    cert_data = {"citizen_id": 1, "type": "Antecedentes", "status": "Issued"}
    response = client.post("/api/justice/certificates/", json=cert_data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json()["type"] == "Antecedentes"


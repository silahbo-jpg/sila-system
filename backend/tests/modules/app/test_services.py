import pytest
from sqlalchemy.orm import Session
from app.modules.justice import services, schemas

# Exemplo de teste para emissão de certidão

def test_issue_certificate(db: Session, mocker):
    cert_data = schemas.JudicialCertificateCreate(citizen_id=1, type="Execuções", status="Issued")
    mocker.patch("app.utils.pdf_generator.generate_pdf", return_value="/tmp/certificate_1.pdf")
    cert = services.issue_certificate(db, cert_data)
    assert cert.document_path == "/tmp/certificate_1.pdf"
    assert cert.type == "Execuções"
    assert cert.status == "Issued"


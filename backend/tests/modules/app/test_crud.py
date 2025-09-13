import pytest
from sqlalchemy.orm import Session
from app.modules.justice import crud, schemas

def test_create_certificate(db: Session):
    cert_data = schemas.JudicialCertificateCreate(citizen_id=1, type="Antecedentes", status="Issued")
    cert = crud.create_certificate(db, cert_data)
    assert cert.id
    assert cert.type == "Antecedentes"
    assert cert.status == "Issued"

def test_get_certificate(db: Session):
    cert_data = schemas.JudicialCertificateCreate(citizen_id=1, type="Protestos", status="Pending")
    cert = crud.create_certificate(db, cert_data)
    fetched = crud.get_certificate(db, cert.id)
    assert fetched.id == cert.id


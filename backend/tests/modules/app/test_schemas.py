"""
Testes para os esquemas (schemas) do módulo de justiça.

Este módulo contém testes para as validações e regras de negócio
definidas nos esquemas do módulo de justiça.
"""
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.modules.justice.schemas import (
    JudicialCertificateCreate,
    JudicialCertificate,
    MediationRequestCreate,
    JudicialProcessCreate,
    JudicialProcess,
    CertificateType,
    ProcessStatus,
    MediationType
)

class TestJudicialCertificateSchemas:
    """Testes para os esquemas de certificados judiciais."""
    
    def test_certificate_create_valid(self):
        """Testa a criação de um certificado válido."""
        data = {
            "type": "good_conduct",
            "citizenId": 1,
            "details": "Certidão de antecedentes criminais para fins de emprego"
        }
        cert = JudicialCertificateCreate(**data)
        
        assert cert.type == CertificateType.GOOD_CONDUCT
        assert cert.citizen_id == 1
        assert "emprego" in cert.details.lower()
    
    def test_certificate_create_invalid_type(self):
        """Testa a criação com tipo de certificado inválido."""
        with pytest.raises(ValueError):
            JudicialCertificateCreate(
                type="invalid_type",
                citizenId=1,
                details="Detalhes"
            )
    
    def test_certificate_create_missing_details(self):
        """Testa a criação sem detalhes quando são obrigatórios."""
        with pytest.raises(ValueError) as exc_info:
            JudicialCertificateCreate(
                type="good_conduct",
                citizenId=1,
                details=""  # Muito curto
            )
        assert "pelo menos 10" in str(exc_info.value).lower()
    
    def test_certificate_full_model(self):
        """Testa o modelo completo de certificado com dados simulados."""
        issue_date = datetime.now()
        cert = JudicialCertificate(
            id=1,
            type="good_conduct",
            status="completed",
            issueDate=issue_date,
            citizenId=1,
            documentPath="https://example.com/certificates/1.pdf"
        )
        
        assert cert.id == 1
        assert cert.issue_date == issue_date
        assert cert.document_path == "https://example.com/certificates/1.pdf"


class TestMediationRequestSchemas:
    """Testes para os esquemas de solicitações de mediação."""
    
    def test_mediation_request_valid(self):
        """Testa a criação de uma solicitação de mediação válida."""
        data = {
            "type": "neighbor",
            "citizenId": 1,
            "description": "Conflito com vizinho sobre barulho excessivo após as 22h"
        }
        request = MediationRequestCreate(**data)
        
        assert request.type == MediationType.NEIGHBOR
        assert request.citizen_id == 1
        assert len(request.description) >= 20
    
    def test_mediation_request_short_description(self):
        """Testa descrição muito curta na solicitação de mediação."""
        with pytest.raises(ValueError) as exc_info:
            MediationRequestCreate(
                type="neighbor",
                citizenId=1,
                description="Muito curto"
            )
        assert "pelo menos 20" in str(exc_info.value).lower()


class TestJudicialProcessSchemas:
    """Testes para os esquemas de processos judiciais."""
    
    def test_process_create_valid(self):
        """Testa a criação de um processo judicial válido."""
        data = {
            "processNumber": "1234567-89.1234.5.67.8901",
            "court": "1ª Vara Cível de São Paulo",
            "citizenId": 1,
            "status": "pending"
        }
        process = JudicialProcessCreate(**data)
        
        assert process.process_number == "1234567-89.1234.5.67.8901"
        assert process.citizen_id == 1
        assert process.status == ProcessStatus.PENDING
    
    def test_process_invalid_number_format(self):
        """Testa número de processo em formato inválido."""
        with pytest.raises(ValueError) as exc_info:
            JudicialProcessCreate(
                processNumber="123.45.6789-0",  # Formato inválido
                court="1ª Vara",
                citizenId=1
            )
        assert "inválido" in str(exc_info.value).lower()
    
    def test_process_full_model(self):
        """Testa o modelo completo de processo judicial."""
        created_at = datetime.now() - timedelta(days=30)
        updated_at = datetime.now()
        
        process = JudicialProcess(
            id=1,
            processNumber="1234567-89.1234.5.67.8901",
            court="1ª Vara Cível",
            status="in_progress",
            citizenId=1,
            createdAt=created_at,
            updatedAt=updated_at
        )
        
        assert process.id == 1
        assert process.created_at == created_at
        assert process.updated_at == updated_at
        assert process.status == ProcessStatus.IN_PROGRESS


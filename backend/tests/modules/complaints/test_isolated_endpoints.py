"""Testes de integração independentes para os endpoints do módulo de reclamações."""

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from typing import Dict, Any, List, Optional


# Cria um app FastAPI mínimo para testes
app = FastAPI()


# Mock do serviço de reclamações
class MockComplaintService:
    """Implementação mock do serviço de reclamações."""
    
    def __init__(self):
        self.complaints = {}
        self.comments = {}
        self.next_id = 1
    
    async def get_complaints(
        self, 
        skip: int = 0, 
        limit: int = 100, 
        filters: Any = None
    ) -> List[Dict[str, Any]]:
        """Obtém reclamações com filtros."""
        return list(self.complaints.values())[skip:skip+limit]
    
    async def get_complaint(self, complaint_id: int) -> Optional[Dict[str, Any]]:
        """Obtém uma reclamação por ID."""
        return self.complaints.get(complaint_id)
    
    async def create_complaint(
        self, 
        complaint_data: Dict[str, Any], 
        user_id: int
    ) -> Dict[str, Any]:
        """Cria uma nova reclamação."""
        complaint_id = self.next_id
        self.next_id += 1
        
        complaint = {
            "id": complaint_id,
            "title": complaint_data["title"],
            "description": complaint_data["description"],
            "status": "aberta",
            "category": complaint_data["category"],
            "priority": complaint_data.get("priority", "normal"),
            "user_id": user_id,
            "created_at": "2023-10-01T10:00:00",
            "updated_at": "2023-10-01T10:00:00"
        }
        
        self.complaints[complaint_id] = complaint
        return complaint
    
    async def create_comment(
        self, 
        complaint_id: int,
        comment_data: Dict[str, Any],
        user_id: int
    ) -> Dict[str, Any]:
        """Adiciona um comentário a uma reclamação."""
        comment_id = len(self.comments) + 1
        comment = {
            "id": comment_id,
            "complaint_id": complaint_id,
            "user_id": user_id,
            "comment": comment_data["comment"],
            "is_internal": comment_data.get("is_internal", False),
            "created_at": "2023-10-01T10:00:00"
        }
        
        self.comments[comment_id] = comment
        return comment
    
    async def update_complaint(
        self, 
        complaint_id: int, 
        update_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Atualiza uma reclamação."""
        if complaint_id not in self.complaints:
            return None
        
        # Atualiza os campos fornecidos
        for key, value in update_data.items():
            if value is not None:
                self.complaints[complaint_id][key] = value
        
        # Atualiza a data de atualização
        self.complaints[complaint_id]["updated_at"] = "2023-10-01T11:00:00"
        
        return self.complaints[complaint_id]


# Mock do serviço
def get_mock_complaint_service():
    """Retorna uma instância do serviço mock."""
    return MockComplaintService()


# Mock do usuário autenticado
def get_mock_current_user():
    """Retorna um usuário mock para autenticação."""
    return {"id": 1, "username": "testuser", "roles": ["postgres"]}


# Importa e configura as rotas do módulo
from app.modules.complaints.endpoints import router as complaints_router


# Configura as rotas no app de teste
app.include_router(complaints_router, prefix="/api/complaints")


# Aplica os mocks aos serviços reais
app.dependency_overrides[
    app.dependency_overrides.get("get_complaint_service", get_mock_complaint_service)
] = get_mock_complaint_service

app.dependency_overrides[
    app.dependency_overrides.get("get_current_user", get_mock_current_user)
] = get_mock_current_user


# Cliente de teste
client = TestClient(app)


# Testes
def test_list_complaints():
    """Testa o endpoint de listagem de reclamações."""
    response = client.get("/api/complaints/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_create_complaint():
    """Testa o endpoint de criação de reclamação."""
    complaint_data = {
        "title": "Buraco na rua",
        "description": "Buraco grande na avenida",
        "category": "infraestrutura",
        "priority": "alta"
    }
    
    response = client.post("/api/complaints/", json=complaint_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == complaint_data["title"]
    assert data["status"] == "aberta"


# Executa os testes diretamente
if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__] + sys.argv[1:]))


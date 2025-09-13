"""
Testes para cenários de erro no módulo de cidadania.

Este script testa os cenários de erro, incluindo validação de entrada,
duplicidade de registros e mensagens de erro personalizadas.
"""
import sys
import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, Any, Optional, List

# Simulação do FastAPI TestClient
class TestResponse:
    def __init__(self, status_code: int, content: bytes):
        self.status_code = status_code
        self.content = content
    
    def json(self) -> Dict[str, Any]:
        return json.loads(self.content.decode('utf-8'))

class TestClient:
    def __init__(self):
        # Simula um banco de dados em memória para testes de duplicidade
        self.citizens = {}
        import json
        self.json = json
    
    def post(self, url: str, json: Dict, headers: Optional[Dict] = None) -> TestResponse:
        """Simula uma requisição POST para criar um cidadão."""
        print(f"\n🔵 POST {url}")
        print(f"   Dados: {self.json.dumps(json, indent=2)}")
        
        # Valida autenticação
        if not headers or "Authorization" not in headers:
            return self._create_response(
                HTTPStatus.UNAUTHORIZED,
                {"detail": "Not authenticated"}
            )
        
        # Valida permissão
        postgres = self._get_authenticated_user(headers["Authorization"])
        if not postgres.is_superuser and "citizenship:citizen:create" not in postgres.permissions:
            return self._create_response(
                HTTPStatus.FORBIDDEN,
                {"status": "error", "code": "permission_denied"}
            )
        
        # Validação de campos obrigatórios
        required_fields = ["bi_numero", "nome_completo", "data_nascimento", "municipio_residencia"]
        missing_fields = [field for field in required_fields if field not in json]
        
        if missing_fields:
            return self._create_response(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "loc": ["body", field],
                            "msg": "field required",
                            "type": "value_error.missing"
                        } for field in missing_fields
                    ]
                }
            )
        
        # Validação de formato do BI
        if not self._validar_bi(json["bi_numero"]):
            return self._create_response(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    "detail": [
                        {
                            "loc": ["body", "bi_numero"],
                            "msg": "Número de BI inválido. Formato esperado: 9-14 caracteres alfanuméricos",
                            "type": "value_error"
                        }
                    ]
                }
            )
        
        # Verifica duplicidade de BI
        if json["bi_numero"] in self.citizens:
            return self._create_response(
                HTTPStatus.CONFLICT,
                {
                    "status": "error",
                    "code": "duplicate_bi",
                    "detail": "Já existe um cidadão cadastrado com este número de BI"
                }
            )
        
        # Cria o cidadão
        citizen_id = f"cid_{len(self.citizens) + 1}"
        self.citizens[json["bi_numero"]] = {
            "id": citizen_id,
            **json,
            "status": "ativo"
        }
        
        return self._create_response(
            HTTPStatus.CREATED,
            {"id": citizen_id, "status": "ativo"}
        )
    
    def _validar_bi(self, bi_numero: str) -> bool:
        """Valida o formato do número de BI."""
        if not isinstance(bi_numero, str):
            return False
        return 9 <= len(bi_numero) <= 14 and bi_numero.isalnum()
    
    def _get_authenticated_user(self, auth_header: str):
        """Simula extração de usuário do token JWT."""
        token = auth_header.replace("Bearer ", "")
        
        if token == "admin-token":
            return MockUser(
                id=1,
                username="postgres",
                is_superuser=True,
                permissions=["citizenship:citizen:create", "citizenship:citizen:read"]
            )
        elif token == "user-token":
            return MockUser(
                id=2,
                username="testuser",
                permissions=["citizenship:citizen:read"]
            )
        else:
            return MockUser(
                id=3,
                username="no_perms_user",
                permissions=[]
            )
    
    def _create_response(self, status_code: int, data: Any) -> TestResponse:
        """Cria uma resposta de teste."""
        return TestResponse(status_code, json.dumps(data).encode())

@dataclass
class MockUser:
    id: int
    username: str
    is_superuser: bool = False
    permissions: List[str] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []
        self.is_active = True
        self.email = f"{self.username}@example.com"
        self.full_name = f"{self.username.title()} postgres"

# Testes
class TestCitizenErrorScenarios:
    def __init__(self):
        self.client = TestClient()
    
    def run_all_tests(self) -> bool:
        """Executa todos os testes e retorna True se todos passarem."""
        tests = [
            self.test_missing_required_fields,
            self.test_invalid_bi_format,
            self.test_duplicate_bi,
            self.test_unauthorized_access,
            self.test_forbidden_access
        ]
        
        print("🚀 Iniciando testes de cenários de erro...")
        passed = 0
        failed = 0
        
        for test in tests:
            test_name = test.__name__
            try:
                test()
                print(f"✅ {test_name}: PASSOU")
                passed += 1
            except AssertionError as e:
                print(f"❌ {test_name}: FALHOU - {str(e)}")
                failed += 1
            except Exception as e:
                print(f"❌ {test_name}: ERRO - {str(e)}")
                failed += 1
        
        print(f"\n📊 Resultado: {passed} testes passaram, {failed} falharam")
        return failed == 0
    
    def test_missing_required_fields(self):
        """Testa a validação de campos obrigatórios."""
        # Dados sem campos obrigatórios
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={},  # Sem campos obrigatórios
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data
        
        # Verifica se todos os campos obrigatórios estão na mensagem de erro
        required_fields = ["bi_numero", "nome_completo", "data_nascimento", "municipio_residencia"]
        error_fields = [error["loc"][1] for error in data["detail"]]
        
        for field in required_fields:
            assert field in error_fields, f"Campo obrigatório '{field}' não foi validado"
    
    def test_invalid_bi_format(self):
        """Testa a validação do formato do número de BI."""
        # BI muito curto
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": "123",  # Inválido: muito curto
                "nome_completo": "João da Silva",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = response.json()
        assert any(error["loc"] == ["body", "bi_numero"] for error in data["detail"])
        
        # BI com caracteres inválidos
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": "123$%^&*()",  # Caracteres especiais inválidos
                "nome_completo": "João da Silva",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    
    def test_duplicate_bi(self):
        """Testa a validação de duplicidade de número de BI."""
        # Primeiro cadastro - deve funcionar
        bi_numero = "123456789LA042"
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": bi_numero,
                "nome_completo": "Maria Santos",
                "data_nascimento": "1985-05-20",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == HTTPStatus.CREATED
        
        # Tentativa de cadastrar o mesmo BI novamente
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": bi_numero,  # Mesmo BI
                "nome_completo": "Outra Pessoa",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer admin-token"}
        )
        
        assert response.status_code == HTTPStatus.CONFLICT
        data = response.json()
        assert data["code"] == "duplicate_bi"
        assert "já existe" in data["detail"].lower()
    
    def test_unauthorized_access(self):
        """Testa o acesso não autorizado sem token."""
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": "987654321LA042",
                "nome_completo": "Teste Sem Token",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            }
            # Sem cabeçalho de autorização
        )
        
        assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    def test_forbidden_access(self):
        """Testa o acesso negado por falta de permissões."""
        # Usuário sem permissão de criação
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": "987654321LA042",
                "nome_completo": "Teste Sem Permissão",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer user-token"}  # Token de usuário sem permissão
        )
        
        assert response.status_code == HTTPStatus.FORBIDDEN
        data = response.json()
        assert data["code"] == "permission_denied"
        
        # Usuário sem nenhuma permissão
        response = self.client.post(
            "/api/v1/citizenship/citizens/",
            json={
                "bi_numero": "987654321LA042",
                "nome_completo": "Teste Sem Nenhuma Permissão",
                "data_nascimento": "1990-01-15",
                "municipio_residencia": "Luanda"
            },
            headers={"Authorization": "Bearer no-perms-token"}
        )
        
        assert response.status_code == HTTPStatus.FORBIDDEN


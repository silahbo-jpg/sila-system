"""
Testes de performance e carga para o módulo de Citizenship.

Este script utiliza o Locust para testar a performance dos endpoints críticos
do módulo de Citizenship sob diferentes cargas de trabalho.

Para executar:
1. Instale as dependências: pip install -r requirements.txt
2. Execute o servidor de desenvolvimento
3. Execute: locust -f citizenship_load_test.py --host=http://localhost:8000
4. Acesse http://localhost:8089 para ver a interface web
"""
import os
import json
from locust import HttpUser, task, between
from faker import Faker
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração
BASE_URL = "/api/citizenship"
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "postgres")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Truman1_Marcelo1_1985")

fake = Faker('pt_BR')

class AuthMixin:
    """Mixin para autenticação de usuários nos testes."""
    
    def login(self, email, Truman1_Marcelo1_1985):
        """Realiza login e retorna o token de acesso."""
        response = self.client.post(
            "/api/auth/login",
            json={"email": email, "Truman1_Marcelo1_1985": Truman1_Marcelo1_1985}
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def get_auth_headers(self, token):
        """Retorna os headers de autenticação."""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

class CitizenTestUser(HttpUser, AuthMixin):
    """Classe de usuário para testar operações de cidadão."""
    
    # Tempo de espera entre requisições (em segundos)
    wait_time = between(1, 5)
    
    def on_start(self):
        """Executado quando um usuário inicia a sessão de teste."""
        self.token = self.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        self.headers = self.get_auth_headers(self.token)
    
    @task(3)  # Maior peso para operações de leitura
    def list_citizens(self):
        """Testa a listagem de cidadãos."""
        self.client.get(
            f"{BASE_URL}/citizens/",
            headers=self.headers,
            name="List Citizens"
        )
    
    @task(2)
    def get_citizen(self):
        """Testa a obtenção de um cidadão específico."""
        # Assumindo que existe pelo menos um cidadão com ID 1
        self.client.get(
            f"{BASE_URL}/citizens/1",
            headers=self.headers,
            name="Get Citizen"
        )
    
    @task(1)  # Menor peso para operações de escrita
    def create_citizen(self):
        """Testa a criação de um novo cidadão."""
        citizen_data = {
            "nome_completo": fake.name(),
            "numero_bi": fake.random_number(digits=9, fix_len=True),
            "cpf": fake.random_number(digits=11, fix_len=True),
            "data_nascimento": fake.date_of_birth().isoformat(),
            "genero": fake.random_element(["M", "F"]),
            "estado_civil": fake.random_element(["SOLTEIRO", "CASADO", "DIVORCIADO", "VIUVO"]),
            "nome_mae": fake.name_female(),
            "nome_pai": fake.name_male(),
            "naturalidade": fake.city(),
            "nacionalidade": "Brasileiro",
            "morada": fake.street_address(),
            "bairro": fake.bairro(),
            "municipio": fake.city(),
            "provincia": fake.estado_nome(),
            "telefone": fake.phone_number(),
            "email": fake.email()
        }
        
        self.client.post(
            f"{BASE_URL}/citizens/",
            json=citizen_data,
            headers=self.headers,
            name="Create Citizen"
        )

class AtestadoTestUser(HttpUser, AuthMixin):
    """Classe de usuário para testar operações de atestado."""
    
    wait_time = between(2, 10)  # Mais tempo entre requisições para operações de atestado
    
    def on_start(self):
        """Executado quando um usuário inicia a sessão de teste."""
        self.token = self.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        self.headers = self.get_auth_headers(self.token)
    
    @task(2)
    def solicitar_atestado(self):
        """Testa a solicitação de um atestado."""
        atestado_data = {
            "tipo": "RESIDENCIA",
            "descricao": fake.sentence(),
            "cidadania_id": 1  # Assumindo que existe um cidadão com ID 1
        }
        
        self.client.post(
            f"{BASE_URL}/atestados/solicitar",
            json=atestado_data,
            headers=self.headers,
            name="Solicitar Atestado"
        )
    
    @task(3)
    def listar_atestados(self):
        """Testa a listagem de atestados."""
        self.client.get(
            f"{BASE_URL}/atestados/",
            headers=self.headers,
            name="Listar Atestados"
        )

class ReportTestUser(HttpUser, AuthMixin):
    """Classe de usuário para testar geração de relatórios."""
    
    wait_time = between(5, 15)  # Mais tempo entre requisições para relatórios
    
    def on_start(self):
        """Executado quando um usuário inicia a sessão de teste."""
        self.token = self.login(ADMIN_EMAIL, ADMIN_PASSWORD)
        self.headers = self.get_auth_headers(self.token)
    
    @task(1)
    def get_summary(self):
        """Testa a obtenção do resumo estatístico."""
        self.client.get(
            f"{BASE_URL}/summary",
            headers=self.headers,
            name="Get Summary"
        )
    
    @task(1)
    def generate_pdf(self):
        """Testa a geração de PDF de um atestado."""
        # Assumindo que existe um atestado com ID 1
        self.client.get(
            f"{BASE_URL}/atestados/1/pdf",
            headers=self.headers,
            name="Generate PDF"
        )


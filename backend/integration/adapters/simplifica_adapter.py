import requests
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

from ...governance.models.audit_log import AuditLog

logger = logging.getLogger(__name__)

class SimplificaAdapter:
    """Adaptador para integração com o sistema SIMPLIFICA 2.0.
    
    Esta classe fornece métodos para interagir com a API do SIMPLIFICA 2.0,
    permitindo sincronização de cadastros, validação de documentos e
    compartilhamento de informações sobre licenciamentos.
    """
    
    def __init__(self, api_url: str, SECRET_KEY_PLACEHOLDER: str, timeout: int = 30):
        """Inicializa o adaptador com as configurações necessárias.
        
        Args:
            api_url: URL base da API do SIMPLIFICA 2.0
            SECRET_KEY_PLACEHOLDER: Chave de API para autenticação
            timeout: Tempo limite para requisições em segundos
        """
        self.api_url = api_url.rstrip('/')
        self.SECRET_KEY_PLACEHOLDER = SECRET_KEY_PLACEHOLDER
        self.timeout = timeout
        self.headers = {
            'Authorization': f'Bearer {self.SECRET_KEY_PLACEHOLDER}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Realiza uma requisição para a API do SIMPLIFICA 2.0.
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API (sem a URL base)
            data: Dados a serem enviados no corpo da requisição
            
        Returns:
            Resposta da API em formato de dicionário
            
        Raises:
            requests.RequestException: Erro na requisição HTTP
            ValueError: Erro na resposta da API
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers, params=data, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers, json=data, timeout=self.timeout)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            response.raise_for_status()
            
            # Registra a operação no log de auditoria
            AuditLog.log_action(
                user_id=0,  # Sistema
                action=f"SIMPLIFICA_{method.upper()}",
                resource_type="SIMPLIFICA_API",
                resource_id=endpoint,
                details={
                    "url": url,
                    "method": method,
                    "status_code": response.status_code,
                    "request_data": data if data else None
                }
            )
            
            return response.json()
        
        except requests.RequestException as e:
            logger.error(f"Erro na requisição para SIMPLIFICA 2.0: {str(e)}")
            
            # Registra o erro no log de auditoria
            AuditLog.log_action(
                user_id=0,  # Sistema
                action="SIMPLIFICA_ERROR",
                resource_type="SIMPLIFICA_API",
                resource_id=endpoint,
                details={
                    "url": url,
                    "method": method,
                    "error": str(e),
                    "request_data": data if data else None
                }
            )
            
            raise
    
    def validate_citizen_document(self, document_type: str, document_number: str) -> Dict:
        """Valida um documento de cidadão no SIMPLIFICA 2.0.
        
        Args:
            document_type: Tipo de documento (BI, Passaporte, etc.)
            document_number: Número do documento
            
        Returns:
            Informações de validação do documento
        """
        endpoint = "api/v1/documents/validate"
        data = {
            "document_type": document_type,
            "document_number": document_number
        }
        
        return self._make_request("POST", endpoint, data)
    
    def sync_citizen(self, citizen_data: Dict) -> Dict:
        """Sincroniza dados de um cidadão com o SIMPLIFICA 2.0.
        
        Args:
            citizen_data: Dados do cidadão a serem sincronizados
            
        Returns:
            Resposta da sincronização
        """
        endpoint = "api/v1/citizens/sync"
        return self._make_request("POST", endpoint, citizen_data)
    
    def get_citizen_by_document(self, document_type: str, document_number: str) -> Optional[Dict]:
        """Busca um cidadão pelo documento no SIMPLIFICA 2.0.
        
        Args:
            document_type: Tipo de documento (BI, Passaporte, etc.)
            document_number: Número do documento
            
        Returns:
            Dados do cidadão ou None se não encontrado
        """
        endpoint = "api/v1/citizens/search"
        data = {
            "document_type": document_type,
            "document_number": document_number
        }
        
        try:
            result = self._make_request("GET", endpoint, data)
            return result.get("citizen")
        except requests.HTTPError as e:
            if e.response.status_code == 404:
                return None
            raise
    
    def share_license_info(self, license_data: Dict) -> Dict:
        """Compartilha informações sobre licenciamento com o SIMPLIFICA 2.0.
        
        Args:
            license_data: Dados do licenciamento a serem compartilhados
            
        Returns:
            Resposta do compartilhamento
        """
        endpoint = "api/v1/licenses/share"
        return self._make_request("POST", endpoint, license_data)
    
    def get_license_status(self, license_number: str) -> Dict:
        """Obtém o status de um licenciamento no SIMPLIFICA 2.0.
        
        Args:
            license_number: Número do licenciamento
            
        Returns:
            Status do licenciamento
        """
        endpoint = f"api/v1/licenses/{license_number}/status"
        return self._make_request("GET", endpoint)
    
    def get_address_validation(self, address: Dict) -> Dict:
        """Valida um endereço no SIMPLIFICA 2.0.
        
        Args:
            address: Dados do endereço a ser validado
            
        Returns:
            Informações de validação do endereço
        """
        endpoint = "api/v1/addresses/validate"
        return self._make_request("POST", endpoint, address)
    
    def get_municipality_info(self, municipality_code: str) -> Dict:
        """Obtém informações sobre um município no SIMPLIFICA 2.0.
        
        Args:
            municipality_code: Código do município
            
        Returns:
            Informações do município
        """
        endpoint = f"api/v1/municipalities/{municipality_code}"
        return self._make_request("GET", endpoint)
    
    def get_service_catalog(self, category: Optional[str] = None) -> List[Dict]:
        """Obtém o catálogo de serviços do SIMPLIFICA 2.0.
        
        Args:
            category: Categoria de serviços (opcional)
            
        Returns:
            Lista de serviços disponíveis
        """
        endpoint = "api/v1/services/catalog"
        data = {"category": category} if category else None
        result = self._make_request("GET", endpoint, data)
        return result.get("services", [])


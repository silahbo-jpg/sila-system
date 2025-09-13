import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class BNAAdapter:
    """Adaptador para integração com a API do Banco Nacional de Angola (BNA).
    
    Esta classe fornece métodos para interagir com os serviços financeiros do BNA,
    incluindo consulta de taxas de câmbio, validação de contas bancárias e
    processamento de transações interbancárias.
    """
    
    def __init__(self, SECRET_KEY_PLACEHOLDER: str, environment: str = "sandbox"):
        """Inicializa o adaptador BNA.
        
        Args:
            SECRET_KEY_PLACEHOLDER: Chave de API fornecida pelo BNA
            environment: Ambiente de execução ('sandbox' ou 'production')
        """
        self.SECRET_KEY_PLACEHOLDER = SECRET_KEY_PLACEHOLDER
        self.environment = environment
        
        # Configuração dos endpoints baseada no ambiente
        if environment == "production":
            self.base_url = "https://api.bna.ao/v1"
        else:
            self.base_url = "https://sandbox.bna.ao/v1"
    
    def get_exchange_rates(self) -> Dict[str, Any]:
        """Obtém as taxas de câmbio atuais do BNA.
        
        Returns:
            Dicionário contendo as taxas de câmbio para diferentes moedas
        """
        endpoint = f"{self.base_url}/exchange-rates"
        headers = {"Authorization": f"Bearer {self.SECRET_KEY_PLACEHOLDER}"}
        
        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao obter taxas de câmbio: {str(e)}")
            return {"error": str(e)}
    
    def validate_bank_account(self, bank_code: str, account_number: str) -> Dict[str, Any]:
        """Valida uma conta bancária através da API do BNA.
        
        Args:
            bank_code: Código do banco (3 dígitos)
            account_number: Número da conta bancária
            
        Returns:
            Dicionário contendo o status de validação e informações da conta
        """
        endpoint = f"{self.base_url}/accounts/validate"
        headers = {
            "Authorization": f"Bearer {self.SECRET_KEY_PLACEHOLDER}",
            "Content-Type": "application/json"
        }
        payload = {
            "bank_code": bank_code,
            "account_number": account_number
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao validar conta bancária: {str(e)}")
            return {"error": str(e)}
    
    def process_payment(self, 
                       source_account: str, 
                       destination_account: str,
                       amount: float,
                       description: str,
                       reference_id: str) -> Dict[str, Any]:
        """Processa um pagamento interbancário através da API do BNA.
        
        Args:
            source_account: Conta de origem (formato: BANCO:NUMERO)
            destination_account: Conta de destino (formato: BANCO:NUMERO)
            amount: Valor da transação
            description: Descrição da transação
            reference_id: ID de referência único para a transação
            
        Returns:
            Dicionário contendo o resultado do processamento do pagamento
        """
        endpoint = f"{self.base_url}/payments/process"
        headers = {
            "Authorization": f"Bearer {self.SECRET_KEY_PLACEHOLDER}",
            "Content-Type": "application/json"
        }
        payload = {
            "source": source_account,
            "destination": destination_account,
            "amount": amount,
            "description": description,
            "reference": reference_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao processar pagamento: {str(e)}")
            return {"error": str(e)}


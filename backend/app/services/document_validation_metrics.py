"""
Serviço para gerenciamento de métricas de validação de documentos.

Este serviço fornece uma interface unificada para acessar métricas de validação
de documentos, como CPF e CNPJ.
"""
from typing import Dict, Any
from app.core.regras_negocio import ValidadorDocumentos

class DocumentValidationMetrics:
    """Serviço de métricas de validação de documentos."""
    
    @classmethod
    def get_cpf_metrics(cls) -> Dict[str, Any]:
        """
        Retorna as métricas de validação de CPF.
        
        Returns:
            Dict[str, Any]: Dicionário com as métricas de validação de CPF
        """
        return ValidadorDocumentos.get_metrics()
    
    @classmethod
    def get_all_metrics(cls) -> Dict[str, Any]:
        """
        Retorna todas as métricas de validação de documentos.
        
        Returns:
            Dict[str, Any]: Dicionário com todas as métricas de validação
        """
        return {
            "cpf_validation": cls.get_cpf_metrics(),
            # Adicionar outras métricas de validação aqui (CNPJ, etc.)
        }

# Instância global do serviço de métricas
document_validation_metrics = DocumentValidationMetrics()


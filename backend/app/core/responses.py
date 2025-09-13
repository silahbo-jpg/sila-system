"""
Módulo de respostas padronizadas para a API.

Este módulo fornece funções para padronizar as respostas da API,
garantindo consistência nas comunicações entre frontend e backend.
"""
from typing import Any, Dict, List, Optional, TypeVar, Generic, Type
from fastapi.responses import JSONResponse
from fastapi import status as http_status
from pydantic import BaseModel

# Tipo genérico para modelos Pydantic
T = TypeVar('T', bound=BaseModel)

def success_response(
    data: Any = None,
    message: str = "Operação realizada com sucesso.",
    status_code: int = http_status.HTTP_200_OK,
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """Retorna uma resposta de sucesso padronizada.
    
    Args:
        data: Dados a serem retornados na resposta
        message: Mensagem descritiva do sucesso
        status_code: Código HTTP de status (padrão: 200)
        meta: Metadados adicionais (paginacao, etc)
        
    Returns:
        JSONResponse: Resposta HTTP padronizada
    """
    response_data: Dict[str, Any] = {
        "status": "success",
        "message": message,
    }
    
    if data is not None:
        response_data["data"] = data
        
    if meta is not None:
        response_data["meta"] = meta
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )

def error_response(
    message: str = "Ocorreu um erro inesperado.",
    status_code: int = http_status.HTTP_400_BAD_REQUEST,
    errors: Optional[Dict[str, List[str]]] = None,
    error_code: Optional[str] = None
) -> JSONResponse:
    """Retorna uma resposta de erro padronizada.
    
    Args:
        message: Mensagem descritiva do erro
        status_code: Código HTTP de status (padrão: 400)
        errors: Dicionário de erros de validação (campo: [erros])
        error_code: Código de erro personalizado
        
    Returns:
        JSONResponse: Resposta HTTP de erro padronizada
    """
    response_data: Dict[str, Any] = {
        "status": "error",
        "message": message,
    }
    
    if error_code:
        response_data["code"] = error_code
        
    if errors:
        response_data["errors"] = errors
    
    return JSONResponse(
        status_code=status_code,
        content=response_data
    )

def not_found_response(
    resource: str = "Recurso",
    message: Optional[str] = None
) -> JSONResponse:
    """Retorna uma resposta 404 padronizada.
    
    Args:
        resource: Nome do recurso não encontrado
        message: Mensagem personalizada (opcional)
        
    Returns:
        JSONResponse: Resposta 404 padronizada
    """
    if message is None:
        message = f"{resource} não encontrado(a)."
        
    return error_response(
        message=message,
        status_code=http_status.HTTP_404_NOT_FOUND,
        error_code="not_found"
    )

def validation_error_response(
    errors: Dict[str, List[str]],
    message: str = "Erro de validação."
) -> JSONResponse:
    """Retorna uma resposta de erro de validação padronizada.
    
    Args:
        errors: Dicionário de erros de validação
        message: Mensagem de erro principal
        
    Returns:
        JSONResponse: Resposta 422 padronizada
    """
    return error_response(
        message=message,
        status_code=http_status.HTTP_422_UNPROCESSABLE_ENTITY,
        errors=errors,
        error_code="validation_error"
    )

def unauthorized_response(
    message: str = "Não autorizado.",
    error_code: str = "unauthorized"
) -> JSONResponse:
    """Retorna uma resposta 401 padronizada.
    
    Args:
        message: Mensagem de erro
        error_code: Código de erro personalizado
        
    Returns:
        JSONResponse: Resposta 401 padronizada
    """
    return error_response(
        message=message,
        status_code=http_status.HTTP_401_UNAUTHORIZED,
        error_code=error_code
    )

def forbidden_response(
    message: str = "Acesso negado.",
    error_code: str = "forbidden"
) -> JSONResponse:
    """Retorna uma resposta 403 padronizada.
    
    Args:
        message: Mensagem de erro
        error_code: Código de erro personalizado
        
    Returns:
        JSONResponse: Resposta 403 padronizada
    """
    return error_response(
        message=message,
        status_code=http_status.HTTP_403_FORBIDDEN,
        error_code=error_code
    )

class PaginatedResponse(Generic[T]):
    """Classe auxiliar para respostas paginadas."""
    
    def __init__(
        self,
        items: List[T],
        total: int,
        page: int = 1,
        per_page: int = 10
    ):
        self.items = items
        self.total = total
        self.page = page
        self.per_page = per_page
        self.pages = (total + per_page - 1) // per_page if per_page > 0 else 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a resposta paginada para dicionário."""
        return {
            "items": self.items,
            "pagination": {
                "total": self.total,
                "page": self.page,
                "per_page": self.per_page,
                "pages": self.pages,
                "has_prev": self.page > 1,
                "has_next": self.page < self.pages
            }
        }


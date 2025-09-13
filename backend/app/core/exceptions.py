"""
Módulo de exceções personalizadas para a aplicação SILA.
"""
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from typing import Any, Dict, Optional


class SILAException(HTTPException):
    """Classe base para exceções personalizadas do SILA."""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None,
        error_type: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers={"X-Error-Type": error_type} if error_type else None
        )
        self.error_code = error_code or f"ERR_{status_code}"
        self.metadata = metadata or {}


class ResourceNotFound(SILAException):
    """Exceção lançada quando um recurso não é encontrado."""
    
    def __init__(self, resource: str, id: Any, **kwargs):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} com ID {id} não encontrado(a).",
            error_type="not_found",
            **kwargs
        )


class UnauthorizedAccess(SILAException):
    """Exceção lançada quando o acesso não é autorizado."""
    
    def __init__(self, detail: str = "Acesso não autorizado.", **kwargs):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_type="unauthorized",
            **kwargs
        )


class ValidationError(SILAException):
    """Exceção lançada quando há erros de validação."""
    
    def __init__(self, detail: str = "Dados inválidos.", errors: Optional[Dict] = None, **kwargs):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_type="validation_error",
            metadata={"errors": errors} if errors else {},
            **kwargs
        )


class BusinessRuleError(SILAException):
    """Exceção lançada quando uma regra de negócio é violada."""
    
    def __init__(self, detail: str, error_code: str = None, **kwargs):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code or "BUSINESS_RULE_VIOLATION",
            error_type="business_rule_violation",
            **kwargs
        )


class DatabaseError(SILAException):
    """Exceção lançada quando ocorre um erro no banco de dados."""
    
    def __init__(self, detail: str = "Erro no banco de dados.", **kwargs):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_type="database_error",
            **kwargs
        )


# Mapeamento de exceções HTTP para nossas exceções personalizadas
HTTP_EXCEPTIONS = {
    400: {"model": BusinessRuleError},
    401: {"model": UnauthorizedAccess},
    403: {"model": UnauthorizedAccess},
    404: {"model": ResourceNotFound},
    422: {"model": ValidationError},
    500: {"model": DatabaseError},
}


def get_http_exception_handler():
    """Retorna um manipulador de exceções HTTP personalizado."""
    from fastapi import Request
    from fastapi.responses import JSONResponse
    import logging
    
    logger = logging.getLogger(__name__)
    
    async def http_exception_handler(request: Request, exc: HTTPException):
        # Log do erro
        logger.error(
            "Erro HTTP: %s - %s",
            exc.status_code,
            exc.detail,
            exc_info=True,
            extra={
                "status_code": exc.status_code,
                "detail": str(exc.detail),
                "path": request.url.path,
                "method": request.method,
            }
        )
        
        # Formata a resposta de erro
        response_data = {
            "error": {
                "code": getattr(exc, "error_code", f"HTTP_{exc.status_code}"),
                "message": str(exc.detail),
                "type": getattr(exc, "error_type", "http_error"),
            }
        }
        
        # Adiciona metadados adicionais, se disponíveis
        if hasattr(exc, "metadata") and exc.metadata:
            response_data["error"]["details"] = exc.metadata
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_data,
            headers=getattr(exc, "headers", None))
    
    return http_exception_handler


def setup_exception_handlers(app: FastAPI) -> None:
    """Configura os manipuladores de exceção personalizados para a aplicação.
    
    Args:
        app: Instância da aplicação FastAPI
    """
    from fastapi import Request
    from fastapi.responses import JSONResponse
    from fastapi.exceptions import RequestValidationError
    import logging
    
    logger = logging.getLogger(__name__)
    
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Manipulador global para exceções HTTP."""
        # Log do erro
        logger.error(
            "Erro HTTP: %s - %s",
            exc.status_code,
            str(exc.detail),
            extra={
                "status_code": exc.status_code,
                "detail": str(exc.detail),
                "path": request.url.path,
                "method": request.method,
            }
        )
        
        # Formata a resposta de erro
        response_data = {
            "status": "error",
            "message": str(exc.detail),
            "data": None,
            "error": {
                "code": getattr(exc, "error_code", f"HTTP_{exc.status_code}"),
                "type": getattr(exc, "error_type", "http_error"),
            }
        }
        
        # Adiciona metadados adicionais, se disponíveis
        if hasattr(exc, "metadata") and exc.metadata:
            response_data["error"]["details"] = exc.metadata
        
        return JSONResponse(
            status_code=exc.status_code,
            content=response_data,
            headers=getattr(exc, "headers", None))
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Manipulador para erros de validação de requisição."""
        # Log do erro
        logger.error(
            "Erro de validação: %s",
            str(exc),
            extra={
                "status_code": 422,
                "detail": str(exc),
                "errors": exc.errors(),
                "path": request.url.path,
                "method": request.method,
            }
        )
        
        # Formata os erros de validação
        errors = {}
        for error in exc.errors():
            # Extrai o nome do campo (último elemento do caminho)
            field = error["loc"][-1] if error["loc"] else "_general"
            if isinstance(field, str):  # Garante que field é uma string
                errors.setdefault(field, []).append(error["msg"])
        
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Erro de validação nos dados fornecidos.",
                "data": None,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "type": "validation_error",
                    "details": errors
                }
            }
        )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Manipulador global para exceções não tratadas."""
        # Log do erro completo
        import traceback
        logger.error(
            "Erro não tratado: %s",
            str(exc),
            exc_info=True,
            extra={
                "path": request.url.path,
                "method": request.method,
                "traceback": "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            }
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Ocorreu um erro interno no servidor. Por favor, tente novamente mais tarde.",
                "data": None,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "type": "server_error"
                }
            }
        )


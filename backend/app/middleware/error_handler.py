# backend/app/middleware/error_handler.py

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
import logging
import traceback
from typing import Callable, Awaitable, Any, Dict

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:
    """
    Middleware para tratamento global de erros na aplicação.
    
    Este middleware captura exceções não tratadas e retorna respostas padronizadas.
    """
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        # Verifica se é uma requisição HTTP
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        
        request = Request(scope, receive)
        
        try:
            # Processa a requisição
            response = await self.app(scope, receive, send)
            return response
            
        except Exception as exc:
            # Log do erro completo
            logger.error(
                f"Erro não tratado na requisição {request.method} {request.url}: {str(exc)}",
                exc_info=True,
                extra={
                    "request": {
                        "method": request.method,
                        "url": str(request.url),
                        "headers": dict(request.headers),
                        "client": f"{request.client.host}:{request.client.port}" if request.client else None,
                    }
                }
            )
            
            # Prepara a resposta de erro padronizada
            error_detail = {
                "error": {
                    "code": "internal_server_error",
                    "message": "Ocorreu um erro interno no servidor.",
                    "details": str(exc) if str(exc) else None,
                }
            }
            
            # Configura o status code apropriado
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
            # Se for um erro de validação, retorna 422 com detalhes
            if hasattr(exc, "status_code") and exc.status_code == 422:
                status_code = exc.status_code
                error_detail["error"]["code"] = "validation_error"
                error_detail["error"]["message"] = "Erro de validação nos dados fornecidos."
                if hasattr(exc, "errors"):
                    error_detail["error"]["details"] = exc.errors()
            
            # Se for um erro de autenticação/autorização, retorna 401/403
            elif hasattr(exc, "status_code") and exc.status_code in (401, 403):
                status_code = exc.status_code
                error_detail["error"]["code"] = "authentication_error" if status_code == 401 else "authorization_error"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else str(exc)
            
            # Se for um erro de recurso não encontrado, retorna 404
            elif hasattr(exc, "status_code") and exc.status_code == 404:
                status_code = exc.status_code
                error_detail["error"]["code"] = "not_found"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else "Recurso não encontrado."
            
            # Se for um erro de negócio, retorna 400
            elif hasattr(exc, "status_code") and exc.status_code == 400:
                status_code = exc.status_code
                error_detail["error"]["code"] = "bad_request"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else "Requisição inválida."
            
            # Em ambiente de desenvolvimento, inclui o traceback completo
            import os
            if os.getenv("ENV") in ("development", "dev"):
                error_detail["traceback"] = traceback.format_exc().splitlines()
            
            # Retorna a resposta de erro padronizada
            return JSONResponse(
                status_code=status_code,
                content=error_detail,
                headers={"Content-Type": "application/json"}
            )

async def error_handler_middleware(request: Request, call_next: Callable) -> Response:
    """
    Função de middleware para tratamento de erros.
    
    Esta função pode ser usada como um middleware FastAPI padrão.
    """
    try:
        return await call_next(request)
    except Exception as exc:
        # O mesmo tratamento de erro do middleware de classe
        logger.error(
            f"Erro não tratado na requisição {request.method} {request.url}: {str(exc)}",
            exc_info=True,
            extra={
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                    "headers": dict(request.headers),
                    "client": f"{request.client.host}:{request.client.port}" if request.client else None,
                }
            }
        )
        
        error_detail = {
            "error": {
                "code": "internal_server_error",
                "message": "Ocorreu um erro interno no servidor.",
                "details": str(exc) if str(exc) else None,
            }
        }
        
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        
        if hasattr(exc, "status_code"):
            status_code = exc.status_code
            
            if status_code == 422:  # Erro de validação
                error_detail["error"]["code"] = "validation_error"
                error_detail["error"]["message"] = "Erro de validação nos dados fornecidos."
                if hasattr(exc, "errors"):
                    error_detail["error"]["details"] = exc.errors()
            
            elif status_code in (401, 403):  # Erro de autenticação/autorização
                error_detail["error"]["code"] = "authentication_error" if status_code == 401 else "authorization_error"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else str(exc)
            
            elif status_code == 404:  # Recurso não encontrado
                error_detail["error"]["code"] = "not_found"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else "Recurso não encontrado."
            
            elif status_code == 400:  # Requisição inválida
                error_detail["error"]["code"] = "bad_request"
                error_detail["error"]["message"] = str(exc.detail) if hasattr(exc, "detail") else "Requisição inválida."
        
        # Em ambiente de desenvolvimento, inclui o traceback completo
        import os
        if os.getenv("ENV") in ("development", "dev"):
            error_detail["traceback"] = traceback.format_exc().splitlines()
        
        return JSONResponse(
            status_code=status_code,
            content=error_detail,
            headers={"Content-Type": "application/json"}
        )


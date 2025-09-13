"""
Middleware de auditoria para registrar informações detalhadas sobre cada requisição.
Inclui informações de rate limiting, autenticação e outros metadados úteis.
"""
import time
import json
import logging
from typing import Callable, Awaitable, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)

class AuditLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar informações de auditoria de cada requisição.
    
    Registra:
    - Método HTTP e URL
    - Código de status da resposta
    - Tempo de processamento
    - IP do cliente
    - User-Agent
    - Headers relevantes
    - Parâmetros de consulta e corpo (se aplicável)
    - Informações de rate limiting
    """
    
    def __init__(
        self,
        app: ASGIApp,
        *,
        sensitive_headers: set = None,
        log_request_body: bool = True,
        log_response_body: bool = False,
        exclude_paths: list = None) -> None:
        super().__init__(app)
        self.sensitive_headers = sensitive_headers or {"authorization", "cookie", "set-cookie"}
        self.log_request_body = log_request_body
        self.log_response_body = log_response_body
        self.exclude_paths = set(exclude_paths or [])
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Ignorar caminhos excluídos (como health checks)
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Iniciar temporizador
        start_time = time.time()
        
        # Coletar informações da requisição
        request_info = self._extract_request_info(request)
        
        try:
            # Processar a requisição
            response = await call_next(request)
            
            # Calcular tempo de processamento
            process_time = (time.time() - start_time) * 1000
            
            # Coletar informações da resposta
            response_info = self._extract_response_info(response)
            
            # Registrar informações de auditoria
            self._log_audit(
                request_info=request_info,
                response_info=response_info,
                process_time=process_time,
                status="success"
            )
            
            return response
            
        except Exception as e:
            # Registrar erro na auditoria
            process_time = (time.time() - start_time) * 1000
            self._log_audit(
                request_info=request_info,
                response_info={"error": str(e), "type": type(e).__name__},
                process_time=process_time,
                status="error"
            )
            raise
    
    def _extract_request_info(self, request: Request) -> Dict[str, Any]:
        """Extrai informações da requisição para auditoria."""
        # Obter cabeçalhos, filtrando os sensíveis
        headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in self.sensitive_headers
        }
        
        # Obter informações básicas da requisição
        request_info = {
            "method": request.method,
            "url": str(request.url),
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client": {
                "host": request.client.host if request.client else None,
                "port": request.client.port if request.client else None,
            },
            "headers": headers,
        }
        
        # Adicionar corpo da requisição se necessário
        if self.log_request_body and request.method in ("POST", "PUT", "PATCH"):
            try:
                body = request.json()
                request_info["body"] = body
            except (json.JSONDecodeError, AttributeError):
                request_info["body"] = "<binary or non-json content>"
        
        return request_info
    
    def _extract_response_info(self, response: Response) -> Dict[str, Any]:
        """Extrai informações da resposta para auditoria."""
        response_info = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
        }
        
        # Adicionar corpo da resposta se necessário
        if self.log_response_body and hasattr(response, "body"):
            try:
                response_info["body"] = response.body.decode()
            except (UnicodeDecodeError, AttributeError):
                response_info["body"] = "<binary content>"
        
        return response_info
    
    def _log_audit(
        self,
        request_info: Dict[str, Any],
        response_info: Dict[str, Any],
        process_time: float,
        status: str = "success"
    ) -> None:
        """Registra as informações de auditoria."""
        audit_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "status": status,
            "request": request_info,
            "response": response_info,
            "process_time_ms": round(process_time, 2),
        }
        
        # Adicionar informações de rate limiting se disponíveis
        if hasattr(request_info.get("request", {}), "state") and hasattr(request_info["request"].state, "rate_limit"):
            audit_data["rate_limiting"] = {
                "limit": getattr(request_info["request"].state.rate_limit, "limit", None),
                "remaining": getattr(request_info["request"].state.rate_limit, "remaining", None),
                "reset": getattr(request_info["request"].state.rate_limit, "reset", None),
            }
        
        # Registrar no logger
        logger.info(
            "Audit Log",
            extra={"audit_data": audit_data})

# Função auxiliar para adicionar o middleware ao aplicativo FastAPI
def setup_audit_middleware(app):
    """Configura o middleware de auditoria no aplicativo FastAPI."""
    # Caminhos que devem ser ignorados pelo middleware de auditoria
    exclude_paths = [
        "/health",
        "/favicon.ico",
        "/docs",
        "/openapi.json",
        "/redoc",
    ]
    
    # Adicionar o middleware ao aplicativo
    app.add_middleware(
        AuditLogMiddleware,
        exclude_paths=exclude_paths,
        log_request_body=True,
        log_response_body=False)
    
    return app


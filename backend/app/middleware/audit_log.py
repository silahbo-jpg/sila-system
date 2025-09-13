"""
Middleware de Auditoria para SILA
Log automático de ações (create, update, delete) dos usuários
"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import uuid

logger = logging.getLogger(__name__)

class AuditLogMiddleware(BaseHTTPMiddleware):
    """Middleware para logging automático de ações dos usuários"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.audit_logs = []  # Em produção, usar banco de dados
    
    async def dispatch(self, request: Request, call_next):
        """Intercepta requisições para logging de auditoria"""
        
        # Captura informações da requisição
        audit_data = await self._capture_request_data(request)
        
        # Processa a requisição
        response = await call_next(request)
        
        # Captura informações da resposta
        audit_data.update(await self._capture_response_data(response))
        
        # Registra o log de auditoria
        await self._log_audit_event(audit_data)
        
        return response
    
    async def _capture_request_data(self, request: Request) -> Dict[str, Any]:
        """Captura dados da requisição para auditoria"""
        try:
            # Informações básicas da requisição
            audit_data = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_ip": self._get_client_ip(request),
                "user_agent": request.headers.get("user-agent", ""),
                "content_type": request.headers.get("content-type", ""),
                "content_length": request.headers.get("content-length", "0"),
            }
            
            # Captura dados do usuário autenticado (se houver)
            user_info = await self._extract_user_info(request)
            if user_info:
                audit_data.update(user_info)
            
            # Captura body da requisição (apenas para métodos que modificam dados)
            if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
                try:
                    body = await request.body()
                    if body:
                        # Tenta parsear como JSON, senão usa como string
                        try:
                            audit_data["request_body"] = json.loads(body.decode())
                        except:
                            audit_data["request_body"] = body.decode()[:500]  # Limita tamanho
                except Exception as e:
                    audit_data["request_body_error"] = str(e)
            
            return audit_data
            
        except Exception as e:
            logger.error(f"Erro ao capturar dados da requisição: {str(e)}")
            return {"error": str(e)}
    
    async def _capture_response_data(self, response: Response) -> Dict[str, Any]:
        """Captura dados da resposta para auditoria"""
        try:
            return {
                "response_status_code": response.status_code,
                "response_headers": dict(response.headers),
                "response_size": len(response.body) if hasattr(response, 'body') else 0,
            }
        except Exception as e:
            logger.error(f"Erro ao capturar dados da resposta: {str(e)}")
            return {"response_error": str(e)}
    
    def _get_client_ip(self, request: Request) -> str:
        """Extrai IP real do cliente"""
        # Verifica headers de proxy
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    async def _extract_user_info(self, request: Request) -> Optional[Dict[str, Any]]:
        """Extrai informações do usuário autenticado"""
        try:
            # Verifica se há token de autenticação
            auth_header = request.headers.get("authorization")
            if not auth_header:
                return None
            
            # Em produção, decodificar JWT para extrair user_id
            # Por enquanto, mock
            return {
                "user_id": "mock_user_id",
                "user_role": "citizen",
                "authenticated": True
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair informações do usuário: {str(e)}")
            return None
    
    async def _log_audit_event(self, audit_data: Dict[str, Any]):
        """Registra evento de auditoria"""
        try:
            # Determina se é uma ação crítica baseada no método e path
            is_critical = self._is_critical_action(audit_data)
            
            # Adiciona flag de ação crítica
            audit_data["is_critical"] = is_critical
            
            # Log baseado na criticidade
            if is_critical:
                logger.warning(f"🔴 AÇÃO CRÍTICA: {audit_data['method']} {audit_data['path']} - postgres: {audit_data.get('user_id', 'anonymous')}")
            else:
                logger.info(f"📝 AUDIT: {audit_data['method']} {audit_data['path']} - postgres: {audit_data.get('user_id', 'anonymous')}")
            
            # Armazena no "banco" (em produção, usar Prisma)
            self.audit_logs.append(audit_data)
            
            # Limita tamanho da lista em memória
            if len(self.audit_logs) > 1000:
                self.audit_logs = self.audit_logs[-500:]
                
        except Exception as e:
            logger.error(f"Erro ao registrar log de auditoria: {str(e)}")
    
    def _is_critical_action(self, audit_data: Dict[str, Any]) -> bool:
        """Determina se uma ação é crítica baseada no método e path"""
        critical_patterns = [
            # Operações de criação
            ("POST", "/api/citizenship/certificates"),
            ("POST", "/api/commercial/licenses"),
            ("POST", "/api/justice/processes"),
            
            # Operações de exclusão
            ("DELETE", "/api/citizenship"),
            ("DELETE", "/api/commercial"),
            ("DELETE", "/api/justice"),
            
            # Operações administrativas
            ("POST", "/api/postgres"),
            ("PUT", "/api/postgres"),
            ("DELETE", "/api/postgres"),
            
            # Operações de autenticação
            ("POST", "/api/auth/login"),
            ("POST", "/api/auth/logout"),
            ("POST", "/api/auth/register"),
        ]
        
        method = audit_data.get("method", "")
        path = audit_data.get("path", "")
        
        return any(
            pattern_method == method and path.startswith(pattern_path)
            for pattern_method, pattern_path in critical_patterns
        )
    
    async def get_audit_logs(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> list:
        """Busca logs de auditoria com filtros"""
        try:
            logs = self.audit_logs.copy()
            
            # Filtra por usuário
            if user_id:
                logs = [log for log in logs if log.get("user_id") == user_id]
            
            # Filtra por data
            if start_date:
                logs = [log for log in logs if datetime.fromisoformat(log["timestamp"]) >= start_date]
            
            if end_date:
                logs = [log for log in logs if datetime.fromisoformat(log["timestamp"]) <= end_date]
            
            # Ordena por timestamp (mais recente primeiro)
            logs.sort(key=lambda x: x["timestamp"], reverse=True)
            
            # Limita resultados
            return logs[:limit]
            
        except Exception as e:
            logger.error(f"Erro ao buscar logs de auditoria: {str(e)}")
            return []
    
    async def get_critical_actions(self, hours: int = 24) -> list:
        """Busca ações críticas das últimas N horas"""
        try:
            cutoff_time = datetime.utcnow().replace(hour=datetime.utcnow().hour - hours)
            
            critical_logs = [
                log for log in self.audit_logs
                if log.get("is_critical", False) and 
                datetime.fromisoformat(log["timestamp"]) >= cutoff_time
            ]
            
            return critical_logs
            
        except Exception as e:
            logger.error(f"Erro ao buscar ações críticas: {str(e)}")
            return []

# Instância global do middleware
audit_middleware = AuditLogMiddleware 


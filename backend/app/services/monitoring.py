"""
Serviço de monitoramento e métricas para o backend.

Este serviço é responsável por coletar métricas, rastrear erros e gerar alertas
para monitoramento da saúde da aplicação.
"""
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import os
import json
from functools import wraps

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configuração de logging
logger = logging.getLogger(__name__)

# Dicionário para armazenar métricas em memória (em produção, use um serviço como Prometheus)
metrics_store = {
    'http_requests_total': {},
    'http_request_duration_seconds': {},
    'errors_total': {},
    'custom_metrics': {}
}

class MonitoringService:
    """Serviço de monitoramento para coleta de métricas e rastreamento de erros."""
    
    def __init__(self, service_name: str = "sila-backend"):
        """Inicializa o serviço de monitoramento.
        
        Args:
            service_name: Nome do serviço para identificação nos logs e métricas.
        """
        self.service_name = service_name
        self.enabled = os.getenv("ENABLE_MONITORING", "false").lower() == "true"
        self.metrics = metrics_store
        
        # Configuração adicional pode ser adicionada aqui
        self._setup_exception_handlers()
    
    def _setup_exception_handlers(self):
        """Configura manipuladores de exceção globais."""
        import sys
        import traceback
        
        def handle_exception(exc_type, exc_value, exc_traceback):
            """Manipulador global de exceções não capturadas."""
            # Não intercepta exceções de teclado (Ctrl+C)
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
                
            # Registra a exceção
            logger.error(
                "Exceção não capturada:",
                exc_info=(exc_type, exc_value, exc_traceback)
            )
            
            # Incrementa o contador de erros
            error_name = f"{exc_type.__module__}.{exc_type.__name__}"
            self.increment_counter('errors_total', {'type': error_name})
            
            # Em produção, aqui você enviaria o erro para um serviço como Sentry
            if self.enabled:
                self.capture_exception(exc_value)
        
        # Configura o manipulador global de exceções
        sys.excepthook = handle_exception
    
    def capture_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None):
        """Captura uma exceção para rastreamento.
        
        Args:
            exception: A exceção capturada.
            context: Contexto adicional para ajudar no diagnóstico.
        """
        if not self.enabled:
            return
            
        try:
            error_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'service': self.service_name,
                'error': {
                    'type': type(exception).__name__,
                    'message': str(exception),
                    'module': exception.__class__.__module__,
                },
                'context': context or {},
                'environment': os.getenv('ENVIRONMENT', 'development'),
            }
            
            # Em produção, você enviaria esses dados para um serviço como Sentry
            logger.error("Exceção capturada: %s", json.dumps(error_data, default=str))
            
        except Exception as e:
            logger.error("Falha ao capturar exceção: %s", str(e))
    
    def capture_message(self, message: str, level: str = 'info', **kwargs):
        """Captura uma mensagem para rastreamento.
        
        Args:
            message: Mensagem a ser registrada.
            level: Nível de log (info, warning, error, etc.).
            **kwargs: Metadados adicionais.
        """
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': self.service_name,
            'level': level,
            'message': message,
            **kwargs
        }
        
        # Em produção, você enviaria esses dados para um serviço como Sentry
        getattr(logger, level)(json.dumps(log_data, default=str))
    
    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Incrementa um contador de métrica.
        
        Args:
            name: Nome da métrica.
            labels: Rótulos para segmentação da métrica.
        """
        if not self.enabled:
            return
            
        try:
            key = self._get_metric_key(name, labels)
            self.metrics['custom_metrics'].setdefault(key, 0)
            self.metrics['custom_metrics'][key] += 1
            
            logger.debug("Métrica incrementada: %s = %s", key, self.metrics['custom_metrics'][key])
            
        except Exception as e:
            logger.error("Falha ao incrementar métrica %s: %s", name, str(e))
    
    def record_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Registra um valor em um histograma.
        
        Args:
            name: Nome do histograma.
            value: Valor a ser registrado.
            labels: Rótulos para segmentação da métrica.
        """
        if not self.enabled:
            return
            
        try:
            key = self._get_metric_key(name, labels)
            self.metrics.setdefault('histograms', {}).setdefault(key, []).append(value)
            
            # Mantém apenas os últimos 1000 valores para evitar consumo excessivo de memória
            if len(self.metrics['histograms'][key]) > 1000:
                self.metrics['histograms'][key] = self.metrics['histograms'][key][-1000:]
                
            logger.debug("Valor registrado no histograma %s: %s", key, value)
            
        except Exception as e:
            logger.error("Falha ao registrar valor no histograma %s: %s", name, str(e))
    
    def _get_metric_key(self, name: str, labels: Optional[Dict[str, str]] = None) -> str:
        """Gera uma chave única para uma métrica com base em seus rótulos.
        
        Args:
            name: Nome da métrica.
            labels: Rótulos da métrica.
            
        Returns:
            Uma string que representa a chave única da métrica.
        """
        if not labels:
            return name
            
        # Ordena os rótulos para garantir consistência
        sorted_labels = sorted(labels.items(), key=lambda x: x[0])
        label_str = ",".join(f"{k}={v}" for k, v in sorted_labels)
        return f"{name}{{{label_str}}}"
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna as métricas coletadas.
        
        Returns:
            Um dicionário com todas as métricas coletadas.
        """
        return self.metrics
    
    def http_middleware(self):
        """Middleware para rastreamento de requisições HTTP."""
        async def middleware(request: Request, call_next):
            # Ignora requisições para endpoints de monitoramento
            if request.url.path.startswith('/metrics') or request.url.path.startswith('/health'):
                return await call_next(request)
            
            # Registra o início da requisição
            start_time = datetime.utcnow()
            request_id = request.headers.get('X-Request-ID', 'unknown')
            
            # Incrementa o contador de requisições
            self.increment_counter('http_requests_total', {
                'method': request.method,
                'endpoint': request.url.path,
                'status': 'started'
            })
            
            try:
                # Processa a requisição
                response = await call_next(request)
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                # Registra métricas de sucesso
                self.increment_counter('http_requests_total', {
                    'method': request.method,
                    'endpoint': request.url.path,
                    'status': 'completed',
                    'status_code': response.status_code
                })
                
                self.record_histogram('http_request_duration_seconds', duration, {
                    'method': request.method,
                    'endpoint': request.url.path,
                    'status_code': str(response.status_code)
                })
                
                # Adiciona cabeçalhos de rastreamento
                response.headers['X-Request-ID'] = request_id
                response.headers['X-Request-Duration'] = str(duration)
                
                return response
                
            except Exception as e:
                # Registra métricas de erro
                duration = (datetime.utcnow() - start_time).total_seconds()
                
                self.increment_counter('http_requests_total', {
                    'method': request.method,
                    'endpoint': request.url.path,
                    'status': 'error',
                    'error_type': type(e).__name__
                })
                
                self.record_histogram('http_request_duration_seconds', duration, {
                    'method': request.method,
                    'endpoint': request.url.path,
                    'status': 'error',
                    'error_type': type(e).__name__
                })
                
                # Captura a exceção para rastreamento
                self.capture_exception(e, {
                    'request_method': request.method,
                    'request_url': str(request.url),
                    'request_headers': dict(request.headers),
                    'request_duration_seconds': duration
                })
                
                # Re-lança a exceção para o manipulador de erros do FastAPI
                raise
        
        return middleware
    
    def time_operation(self, name: str, labels: Optional[Dict[str, str]] = None):
        """Decorador para medir o tempo de execução de uma função.
        
        Args:
            name: Nome da operação.
            labels: Rótulos adicionais para a métrica.
            
        Returns:
            Um decorador que mede o tempo de execução da função decorada.
        """
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = datetime.utcnow()
                try:
                    result = await func(*args, **kwargs)
                    return result
                finally:
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    self.record_histogram(
                        f"{name}_duration_seconds", 
                        duration,
                        labels
                    )
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = datetime.utcnow()
                try:
                    return func(*args, **kwargs)
                finally:
                    duration = (datetime.utcnow() - start_time).total_seconds()
                    self.record_histogram(
                        f"{name}_duration_seconds", 
                        duration,
                        labels
                    )
            
            return async_wrapper if str(func.__code__.co_flags).endswith('128') else sync_wrapper
        
        return decorator


# Instância global do serviço de monitoramento
monitoring = MonitoringService()


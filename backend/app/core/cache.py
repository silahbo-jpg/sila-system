"""
Módulo para cache assíncrono usando async-lru.
"""
from functools import wraps
from typing import Any, Callable, TypeVar, Optional
from datetime import timedelta
import asyncio
from fastapi import HTTPException, status
import logging

# Tenta importar async_lru, se não estiver disponível, usa um mock
# para não quebrar o código em ambientes de desenvolvimento
async_lru_available = True
try:
    from async_lru import alru_cache
except ImportError:
    async_lru_available = False
    
    # Implementação mock para quando async-lru não estiver disponível
    def alru_cache(*args, **kwargs):
        def decorator(f):
            @wraps(f)
            async def wrapper(*args, **kwargs):
                return await f(*args, **kwargs)
            return wrapper
        return decorator

T = TypeVar('T')

# Configuração de logging
logger = logging.getLogger(__name__)

def async_cache(
    maxsize: int = 128,
    ttl: Optional[float] = None,
    exclude_errors: tuple = (HTTPException)
    ):
    """
    Decorator para cache assíncrono com TTL (Time To Live) opcional.
    
    Args:
        maxsize: Tamanho máximo do cache
        ttl: Tempo de vida do cache em segundos
        exclude_errors: Exceções que não devem ser armazenadas em cache
    """
    def decorator(f: Callable[..., T]) -> Callable[..., T]:
        # Se async_lru não estiver disponível, retorna a função original
        if not async_lru_available:
            logger.warning(
                "async-lru não está instalado. O cache estará desabilitado. "
                "Instale com: pip install async-lru"
            )
            return f
            
        # Cria o cache com o tamanho máximo
        cached_func = alru_cache(maxsize=maxsize)(f)
        
        # Se não houver TTL, retorna o cache simples
        if ttl is None:
            return cached_func
            
        # Se houver TTL, adiciona lógica de expiração
        @wraps(f)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # Gera uma chave única para os argumentos
            cache_key = (args, frozenset(kwargs.items()))
            
            # Verifica se o cache expirou
            current_time = asyncio.get_event_loop().time()
            if not hasattr(wrapper, '_cache_times'):
                wrapper._cache_times = {}
                wrapper._cache = {}
            
            cache_time = wrapper._cache_times.get(cache_key, 0)
            if current_time - cache_time < ttl and cache_key in wrapper._cache:
                return wrapper._cache[cache_key]
                
            # Se o cache expirou ou não existe, chama a função
            try:
                result = await cached_func(*args, **kwargs)
                wrapper._cache[cache_key] = result
                wrapper._cache_times[cache_key] = current_time
                return result
            except exclude_errors as e:
                # Não armazena erros em cache
                raise e
            except Exception as e:
                logger.error(f"Erro ao acessar cache para {f.__name__}: {e}")
                return await f(*args, **kwargs)
                
        return wrapper
        
    return decorator

def clear_caches():
    """Limpa todos os caches decorados com @async_cache."""
    for obj in globals().values():
        if hasattr(obj, 'cache_clear'):
            obj.cache_clear()


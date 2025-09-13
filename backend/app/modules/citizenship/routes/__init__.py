"""
Citizenship Routes Module.

This module collects and combines all route modules for the citizenship functionality.
"""
from fastapi import APIRouter

# Create main router
router = APIRouter()

# Import and include all route modules
from .emissao_bi_route import router as emissao_bi_router
from .atualizacao_b_i import router as atualizacao_bi_router
from .emissao_passaporte import router as passaporte_router
from .atualizacao_endereco import router as endereco_router
from .declaracao_residencia import router as residencia_router
from .certidao_nascimento import router as nascimento_router
from .certidao_obito import router as obito_router
from .certidao_casamento import router as casamento_router
from .regitro_eleitoral import router as eleitoral_router
from .visto_permanencia import router as visto_router

# Include all routers with their respective prefixes
router.include_router(emissao_bi_router, tags=["Emissão de BI"])
router.include_router(atualizacao_bi_router, tags=["Atualização de BI"])
router.include_router(passaporte_router, tags=["Emissão de Passaporte"])
router.include_router(endereco_router, tags=["Atualização de Endereço"])
router.include_router(residencia_router, tags=["Declaração de Residência"])
router.include_router(nascimento_router, tags=["Certidão de Nascimento"])
router.include_router(obito_router, tags=["Certidão de Óbito"])
router.include_router(casamento_router, tags=["Certidão de Casamento"])
router.include_router(eleitoral_router, tags=["Registro Eleitoral"])
router.include_router(visto_router, tags=["Visto de Permanência"])

__all__ = ["router"]

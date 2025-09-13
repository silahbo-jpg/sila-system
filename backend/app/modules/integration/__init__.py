from fastapi import APIRouter
from app.modules.integration.routes import router
from app.modules.integration.integration_gateway import integration_gateway

from app.modules.integration.routes.sincronizacao_b_n_a import router as sincronizacao_b_n_a_router
from app.modules.integration.routes.a_p_i_gateway import router as a_p_i_gateway_router
from app.modules.integration.routes.conector_externo import router as conector_externo_router
from app.modules.integration.routes.transformacao_dados import router as transformacao_dados_router
api_router = APIRouter()
router.include_router(transformacao_dados_router)
router.include_router(conector_externo_router)
router.include_router(a_p_i_gateway_router)
router.include_router(sincronizacao_b_n_a_router)
api_router.include_router(router, prefix="/integration", tags=["integration"])

__all__ = ["api_router", "integration_gateway"]


# Serviço: Sincronização BNA / BNA Synchronization

# Serviço: Gateway de API / API Gateway

# Serviço: Conector Externo / External Connector

# Serviço: Transformação de Dados / Data Transformation

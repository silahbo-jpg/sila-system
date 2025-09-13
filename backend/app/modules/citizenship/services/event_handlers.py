from typing import Dict, Any
import logging
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.integration.models import IntegrationEvent
from app.modules.integration.integration_gateway import integration_gateway
from app.modules.citizenship.services import citizen_service

# Configuração de logging
logger = logging.getLogger("citizenship.event_handlers")

async def handle_document_issued(event: IntegrationEvent, payload: Dict[str, Any]):
    """Manipulador de evento para quando um documento é emitido.
    
    Este handler é chamado quando o módulo de documentos emite um novo documento
    para um cidadão. Ele atualiza o registro do cidadão com a informação do novo documento.
    
    Args:
        event: O evento de integração
        payload: Os dados do evento
    """
    try:
        # Obter dados do payload
        citizen_id = payload.get("citizen_id")
        document_type = payload.get("document_type")
        document_id = payload.get("document_id")
        issue_date = payload.get("issue_date")
        
        if not citizen_id or not document_type or not document_id:
            logger.warning(f"Dados incompletos no evento document.issued: {payload}")
            return
        
        # Obter sessão do banco de dados
        db = next(get_db())
        
        # Atualizar o registro do cidadão
        logger.info(f"Atualizando cidadão {citizen_id} com novo documento {document_type}")
        await citizen_service.update_citizen_documents(
            db=db,
            citizen_id=citizen_id,
            document_data={
                "type": document_type,
                "id": document_id,
                "issue_date": issue_date
            }
        )
        
        logger.info(f"Cidadão {citizen_id} atualizado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao processar evento document.issued: {str(e)}")

async def handle_address_changed(event: IntegrationEvent, payload: Dict[str, Any]):
    """Manipulador de evento para quando o endereço de um cidadão é alterado.
    
    Este handler é chamado quando o módulo de endereços registra uma mudança de endereço
    para um cidadão. Ele atualiza o registro do cidadão com o novo endereço.
    
    Args:
        event: O evento de integração
        payload: Os dados do evento
    """
    try:
        # Obter dados do payload
        citizen_id = payload.get("citizen_id")
        new_address = payload.get("address")
        
        if not citizen_id or not new_address:
            logger.warning(f"Dados incompletos no evento address.changed: {payload}")
            return
        
        # Obter sessão do banco de dados
        db = next(get_db())
        
        # Atualizar o endereço do cidadão
        logger.info(f"Atualizando endereço do cidadão {citizen_id}")
        await citizen_service.update_citizen_address(
            db=db,
            citizen_id=citizen_id,
            address_data=new_address
        )
        
        logger.info(f"Endereço do cidadão {citizen_id} atualizado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao processar evento address.changed: {str(e)}")

# Registrar os handlers de eventos
def register_event_handlers():
    """Registra os handlers de eventos para o módulo de cidadania."""
    logger.info("Registrando handlers de eventos para o módulo de cidadania")
    
    # Registrar handler para evento de documento emitido
    integration_gateway.subscribe(
        module="citizenship",
        event_type="document.issued",
        callback=handle_document_issued
    )
    
    # Registrar handler para evento de endereço alterado
    integration_gateway.subscribe(
        module="citizenship",
        event_type="address.changed",
        callback=handle_address_changed
    )
    
    logger.info("Handlers de eventos registrados com sucesso")


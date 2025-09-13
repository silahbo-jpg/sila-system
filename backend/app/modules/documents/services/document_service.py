from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.modules.documents.models import Document
from app.modules.documents.schemas import DocumentCreate, DocumentUpdate
from app.modules.documents.crud import document_crud
from app.modules.integration.integration_gateway import integration_gateway

# Configuração de logging
logger = logging.getLogger("documents.document_service")

async def create_document(db: Session, document_data: DocumentCreate) -> Document:
    """Cria um novo documento no sistema.
    
    Args:
        db: Sessão do banco de dados
        document_data: Dados do documento a ser criado
        
    Returns:
        O documento criado
    """
    logger.info(f"Criando novo documento do tipo {document_data.document_type}")
    
    # Criar o documento no banco de dados
    document = await document_crud.create(db, obj_in=document_data)
    
    # Publicar evento de documento criado
    await publish_document_issued_event(document)
    
    logger.info(f"Documento criado com sucesso: ID {document.id}")
    return document

async def update_document(db: Session, document_id: str, document_data: DocumentUpdate) -> Optional[Document]:
    """Atualiza um documento existente.
    
    Args:
        db: Sessão do banco de dados
        document_id: ID do documento a ser atualizado
        document_data: Dados atualizados do documento
        
    Returns:
        O documento atualizado ou None se não for encontrado
    """
    logger.info(f"Atualizando documento: ID {document_id}")
    
    # Verificar se o documento existe
    document = await document_crud.get(db, id=document_id)
    if not document:
        logger.warning(f"Documento não encontrado: ID {document_id}")
        return None
    
    # Atualizar o documento
    updated_document = await document_crud.update(db, db_obj=document, obj_in=document_data)
    
    # Se o status foi alterado para 'issued', publicar evento
    if document_data.status == "issued" and document.status != "issued":
        await publish_document_issued_event(updated_document)
    
    logger.info(f"Documento atualizado com sucesso: ID {document_id}")
    return updated_document

async def get_document(db: Session, document_id: str) -> Optional[Document]:
    """Obtém um documento pelo ID.
    
    Args:
        db: Sessão do banco de dados
        document_id: ID do documento
        
    Returns:
        O documento ou None se não for encontrado
    """
    logger.info(f"Buscando documento: ID {document_id}")
    document = await document_crud.get(db, id=document_id)
    
    if not document:
        logger.warning(f"Documento não encontrado: ID {document_id}")
    else:
        logger.info(f"Documento encontrado: ID {document_id}")
    
    return document

async def get_documents_by_citizen(db: Session, citizen_id: str) -> List[Document]:
    """Obtém todos os documentos de um cidadão.
    
    Args:
        db: Sessão do banco de dados
        citizen_id: ID do cidadão
        
    Returns:
        Lista de documentos do cidadão
    """
    logger.info(f"Buscando documentos do cidadão: ID {citizen_id}")
    documents = await document_crud.get_multi_by_citizen(db, citizen_id=citizen_id)
    
    logger.info(f"Encontrados {len(documents)} documentos para o cidadão {citizen_id}")
    return documents

async def publish_document_issued_event(document: Document) -> None:
    """Publica um evento de documento emitido no gateway de integração.
    
    Este método é chamado quando um documento é emitido para um cidadão,
    permitindo que outros módulos sejam nnnnotificados e possam atualizar
    suas informações relacionadas.
    
    Args:
        document: O documento emitido
    """
    try:
        # Preparar payload do evento
        payload = {
            "document_id": document.id,
            "citizen_id": document.citizen_id,
            "document_type": document.document_type,
            "issue_date": document.issue_date.isoformat() if document.issue_date else datetime.now().isoformat(),
            "expiry_date": document.expiry_date.isoformat() if document.expiry_date else None,
            "status": document.status
        }
        
        # Publicar evento no gateway de integração
        logger.info(f"Publicando evento document.issued para o documento {document.id}")
        await integration_gateway.publish(
            event_type="document.issued",
            payload=payload,
            source_module="documents"
        )
        
        logger.info(f"Evento document.issued publicado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao publicar evento document.issued: {str(e)}")
        # Não propagar a exceção para não afetar o fluxo principal


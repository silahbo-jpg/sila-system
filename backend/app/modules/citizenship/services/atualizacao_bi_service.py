from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks

from app.db.session import get_db
from app.modules.citizenship.models.atualizacao_b_i import AtualizacaoBI
from app.modules.citizenship.schemas.atualizacao_b_i import (
    AtualizacaoBICreate,
    AtualizacaoBIRead,
    AtualizacaoBIUpdate,
    DocumentType,
    EstadoCivil,
    Genero
)
from app.modules.citizenship.services.atualizacao_bi_business import BIBusinessRules, BIStatus
from app.modules.citizenship.tasks.atualizacao_bi_tasks import BITaskHandler
from app.core.logging import get_logger
from app.core.security import get_current_user_id, get_current_user_role
from fastapi.background import BackgroundTasks

logger = get_logger(__name__)

class AtualizacaoBIService:
    """Service class for handling BI update operations"""
    
    @staticmethod
    def _map_to_db(data: AtualizacaoBICreate, uploaded_docs: List[str] = None) -> Tuple[Dict[str, Any], List[str]]:
        """
        Map Pydantic model to database model
        Returns (mapped_data, validation_errors)
        """
        validation_errors = []
        
        # Validate document requirements
        is_valid, missing_docs = BIBusinessRules.validate_document_requirements(
            document_type=data.tipo_documento,
            uploaded_docs=uploaded_docs or [],
            birth_date=data.data_nascimento
        )
        
        if not is_valid:
            validation_errors.extend([f"Documento obrigatório em falta: {doc}" for doc in missing_docs])
        
        # Calculate expiry date for the new document
        expiry_date = BIBusinessRules.calculate_expiry_date(data.tipo_documento)
        
        mapped_data = {
            "nome": f"{data.nome_completo} - {data.numero_documento}",
            "nome_en": f"{data.nome_completo} - {data.numero_documento}",
            "descricao": f"Atualização de {data.tipo_documento.value}",
            "descricao_en": f"Update of {data.tipo_documento.value}",
            "status": BIStatus.PENDING,
            "dados_adicionais": {
                "tipo_documento": data.tipo_documento.value,
                "numero_documento": data.numero_documento,
                "nome_completo": data.nome_completo,
                "nome_mae": data.nome_mae,
                "nome_pai": data.nome_pai,
                "data_nascimento": data.data_nascimento.isoformat(),
                "naturalidade": data.naturalidade,
                "nacionalidade": data.nacionalidade,
                "estado_civil": data.estado_civil.value,
                "genero": data.genero.value,
                "altura": data.altura,
                "morada": data.morada,
                "codigo_postal": data.codigo_postal,
                "localidade": data.localidade,
                "telefone": data.telefone,
                "email": data.email,
                "motivo_atualizacao": data.motivo_atualizacao,
                "documentos_apresentados": uploaded_docs or [],
                "documentos_em_falta": missing_docs,
                "data_validade": expiry_date.isoformat(),
                "status_history": [{
                    "status": BIStatus.PENDING,
                    "timestamp": datetime.utcnow().isoformat(),
                    "changed_by": "system",
                    "notes": "Pedido criado"
                }]
            },
            "municipe_id": 0  # Will be set by the caller
        }
        
        return mapped_data, validation_errors

    @classmethod
    def create_bi_update(
        cls,
        db: Session,
        bi_data: AtualizacaoBICreate,
        current_user_id: int,
        background_tasks: BackgroundTasks,
        uploaded_docs: List[str] = None
    ) -> AtualizacaoBI:
        """
        Create a new BI update request
        
        Args:
            db: Database session
            bi_data: BI update data
            current_user_id: ID of the current user
            background_tasks: Background tasks handler
            uploaded_docs: List of uploaded document IDs
            
        Returns:
            AtualizacaoBI: The created BI update request
            
        Raises:
            HTTPException: If there are validation errors or creation fails
        """
        try:
            # Map and validate the data
            mapped_data, validation_errors = cls._map_to_db(bi_data, uploaded_docs)
            
            if validation_errors:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"validation_errors": validation_errors}
                )
            
            # Create the request
            db_bi = AtualizacaoBI(**mapped_data)
            db_bi.municipe_id = current_user_id
            
            db.add(db_bi)
            db.commit()
            db.refresh(db_bi)
            
            # Trigger background tasks
            background_tasks.add_task(
                BITaskHandler.send_status_notification,
                email=bi_data.email,
                request_id=db_bi.id,
                status=BIStatus.PENDING
            )
            
            logger.info(f"Created BI update request with ID: {db_bi.id}")
            return db_bi
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating BI update: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Falha ao criar o pedido de atualização de BI"
            )

    @classmethod
    def get_bi_update(
        cls,
        db: Session,
        bi_id: int,
        current_user_id: int
    ) -> Optional[AtualizacaoBI]:
        """Get a BI update request by ID"""
        bi = db.query(AtualizacaoBI).filter(
            AtualizacaoBI.id == bi_id,
            AtualizacaoBI.municipe_id == current_user_id
        ).first()
        
        if not bi:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BI update request not found"
            )
            
        return bi

    @classmethod
    def list_bi_updates(
        cls,
        db: Session,
        current_user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[AtualizacaoBI]:
        """List all BI update requests for the current user"""
        return db.query(AtualizacaoBI)\
            .filter(AtualizacaoBI.municipe_id == current_user_id)\
            .offset(skip)\
            .limit(limit)\
            .all()

    @classmethod
    def update_bi_request(
        cls,
        db: Session,
        bi_id: int,
        bi_update: AtualizacaoBIUpdate,
        current_user_id: int,
        background_tasks: BackgroundTasks,
        current_user_role: str = "user"
    ) -> Optional[AtualizacaoBI]:
        """
        Update a BI update request
        
        Args:
            db: Database session
            bi_id: ID of the BI update request
            bi_update: Update data
            current_user_id: ID of the current user
            background_tasks: Background tasks handler
            current_user_role: Role of the current user
            
        Returns:
            Optional[AtualizacaoBI]: The updated BI update request
            
        Raises:
            HTTPException: If the update fails or is not allowed
        """
        db_bi = cls.get_bi_update(db, bi_id, current_user_id)
        
        try:
            update_data = bi_update.dict(exclude_unset=True)
            
            # Check if status transition is allowed
            if "status" in update_data:
                if not BIBusinessRules.validate_status_transition(
                    current_status=db_bi.status,
                    new_status=update_data["status"],
                    user_role=current_user_role
                ):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Transição de estado inválida: {db_bi.status} -> {update_data['status']}"
                    )
            
            # Update the request
            for field, value in update_data.items():
                if field in ["status"]:
                    # Handle status changes through the task handler
                    BITaskHandler.handle_status_change(
                        db=db,
                        request_id=bi_id,
                        new_status=value,
                        background_tasks=background_tasks,
                        user_role=current_user_role,
                        notes=bi_update.observacoes
                    )
                elif field == "observacoes":
                    # Add to notes history
                    notes_history = db_bi.dados_adicionais.get("notes_history", [])
                    notes_history.append({
                        "timestamp": datetime.utcnow().isoformat(),
                        "user_id": current_user_id,
                        "note": value
                    })
                    db_bi.dados_adicionais["notes_history"] = notes_history
            
            db_bi.data_atualizacao = datetime.utcnow()
            db.commit()
            db.refresh(db_bi)
            
            logger.info(f"Updated BI update request with ID: {bi_id}")
            return db_bi
            
        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating BI update request {bi_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha ao atualizar o pedido: {str(e)}"
            )

    @classmethod
    def delete_bi_request(
        cls,
        db: Session,
        bi_id: int,
        current_user_id: int
    ) -> bool:
        """Delete a BI update request"""
        db_bi = cls.get_bi_update(db, bi_id, current_user_id)
        
        try:
            db.delete(db_bi)
            db.commit()
            logger.info(f"Deleted BI update request with ID: {bi_id}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting BI update request {bi_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete BI update request"
            )

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, UploadFile, File, Form, Request, Query
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Tuple
import json
import uuid
from datetime import date

from app.db.session import get_db
from app.db.models.user import User
from app.core.auth.security import get_current_user, get_current_active_user
from app.modules.citizenship.services.atualizacao_bi_service import AtualizacaoBIService
from app.modules.citizenship.services.atualizacao_bi_business import BIBusinessRules
from app.modules.citizenship.tasks.atualizacao_bi_tasks import BITaskHandler
from app.modules.citizenship.schemas.atualizacao_b_i import (
    AtualizacaoBICreate,
    AtualizacaoBIRead,
    AtualizacaoBIUpdate,
    AtualizacaoBIList,
    DocumentType
)
from app.core.logging import get_logger
from app.core.config import settings
from app.core.storage import save_uploaded_file, delete_file

logger = get_logger(__name__)
router = APIRouter(
    prefix="/api/atualizacao-bi",
    tags=["Atualização de Bilhete de Identidade"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Não autorizado"},
        status.HTTP_403_FORBIDDEN: {"description": "Acesso negado"},
        status.HTTP_404_NOT_FOUND: {"description": "Recurso não encontrado"},
    },
)

# Allowed file types for document uploads
ALLOWED_FILE_TYPES = {
    "application/pdf": "pdf",
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/jpg": "jpg"
}

# Max file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

async def parse_bi_data(
    bi_data: str = Form(...),
    files: List[UploadFile] = File(None)
) -> tuple[AtualizacaoBICreate, list[str]]:
    """Parse BI data and handle file uploads"""
    try:
        # Parse the JSON data
        data = json.loads(bi_data)
        
        # Handle file uploads
        uploaded_docs = []
        if files:
            for file in files:
                if file.content_type not in ALLOWED_FILE_TYPES:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Tipo de ficheiro não suportado: {file.content_type}"
                    )
                
                if file.size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ficheiro {file.filename} excede o tamanho máximo de 10MB"
                    )
                
                # Generate a unique filename
                file_ext = ALLOWED_FILE_TYPES[file.content_type]
                filename = f"docs/{uuid.uuid4()}.{file_ext}"
                
                # Save the file
                await save_uploaded_file(file, filename)
                uploaded_docs.append(filename)
        
        # Convert to Pydantic model
        bi_create = AtualizacaoBICreate(**data)
        return bi_create, uploaded_docs
        
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dados inválidos. Certifique-se de que os dados estão em formato JSON válido."
        )
    except Exception as e:
        logger.error(f"Error parsing BI data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao processar os dados: {str(e)}"
        )

@router.post(
    "/",
    response_model=AtualizacaoBIRead,
    status_code=status.HTTP_201_CREATED,
    summary="Criar um novo pedido de atualização de BI",
    description="Cria um novo pedido de atualização de Bilhete de Identidade.",
    responses={
        201: {"description": "Pedido criado com sucesso"},
        400: {"description": "Dados inválidos ou incompletos"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def criar_atualizacao_bi(
    request: Request,
    background_tasks: BackgroundTasks,
    bi_data: str = Form(...),
    files: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cria um novo pedido de atualização de Bilhete de Identidade.
    
    - **bi_data**: Dados do pedido em formato JSON
    - **files**: Documentos de suporte (opcional)
    """
    try:
        # Parse BI data and handle file uploads
        bi_create, uploaded_docs = await parse_bi_data(bi_data, files)
        
        # Create the BI update request
        db_bi = AtualizacaoBIService.create_bi_update(
            db=db,
            bi_data=bi_create,
            current_user_id=current_user.id,
            background_tasks=background_tasks,
            uploaded_docs=uploaded_docs
        )
        
        # Add background tasks
        background_tasks.add_task(
            send_bi_update_notification,
            db_bi.id,
            "new_request",
            current_user.email
        )
        
        # Log the successful creation
        logger.info(f"Created BI update request {db_bi.id} for user {current_user.id}")
        
        return db_bi
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating BI update request: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao processar o pedido."
        )

@router.get(
    "/{bi_id}",
    response_model=AtualizacaoBIRead,
    summary="Obter detalhes de um pedido de atualização",
    description="Obtém os detalhes de um pedido de atualização de BI específico.",
    responses={
        200: {"description": "Detalhes do pedido"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Pedido não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def obter_atualizacao_bi(
    bi_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtém os detalhes de um pedido de atualização de BI específico.
    
    - **bi_id**: ID do pedido de atualização
    """
    try:
        logger.info(f"Fetching BI update {bi_id} for user {current_user.id}")
        
        # Get the BI update with proper authorization
        db_bi = AtualizacaoBIService.get_bi_update(
            db=db,
            bi_id=bi_id,
            current_user_id=current_user.id
        )
        
        if not db_bi:
            logger.warning(f"BI update {bi_id} not found or access denied for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido de atualização não encontrado ou acesso negado"
            )
            
        return db_bi
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving BI update {bi_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao obter o pedido"
        )

@router.get(
    "/",
    response_model=List[AtualizacaoBIRead],
    summary="Listar pedidos de atualização",
    description="Lista os pedidos de atualização de BI com suporte a paginação e filtros.",
    responses={
        200: {"description": "Lista de pedidos de atualização"},
        400: {"description": "Parâmetros inválidos"},
        401: {"description": "Não autorizado"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def listar_atualizacoes_bi(
    request: Request,
    skip: int = Query(0, ge=0, description="Número de registos a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registos por página (máx. 100)"),
    status: Optional[str] = Query(None, description="Filtrar por estado do pedido"),
    tipo_documento: Optional[str] = Query(None, description="Filtrar por tipo de documento"),
    data_inicio: Optional[date] = Query(None, description="Filtrar por data de criação (a partir de)"),
    data_fim: Optional[date] = Query(None, description="Filtrar por data de criação (até)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Lista os pedidos de atualização de BI com base nos filtros fornecidos.
    
    - **skip**: Número de registos a saltar (para paginação)
    - **limit**: Número máximo de registos por página (máx. 100)
    - **status**: Filtrar por estado do pedido (opcional)
    - **tipo_documento**: Filtrar por tipo de documento (opcional)
    - **data_inicio**: Filtrar por data de criação a partir de (opcional)
    - **data_fim**: Filtrar por data de criação até (opcional)
    """
    try:
        logger.info(f"Listing BI updates for user {current_user.id} with filters: {request.query_params}")
        
        # Build filters
        filters = {
            "status": status,
            "tipo_documento": tipo_documento,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "user_id": None if current_user.role == "admin" else current_user.id
        }
        
        # Get paginated results
        bi_updates = AtualizacaoBIService.list_bi_updates(
            db=db,
            current_user_id=current_user.id,
            skip=skip,
            limit=limit,
            filters=filters
        )
        
        # Add pagination headers
        response_headers = {
            "X-Total-Count": str(len(bi_updates)),
            "X-Page-Size": str(limit),
            "X-Page-Start": str(skip)
        }
        
        return JSONResponse(
            content=jsonable_encoder(bi_updates),
            headers=response_headers
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing BI updates: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao listar os pedidos"
        )

@router.put(
    "/{bi_id}",
    response_model=AtualizacaoBIRead,
    summary="Atualizar um pedido de atualização",
    description="Atualiza um pedido de atualização de BI existente, incluindo alterações de estado e documentos.",
    responses={
        200: {"description": "Pedido atualizado com sucesso"},
        400: {"description": "Dados inválidos ou transição de estado não permitida"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Pedido não encontrado"},
        409: {"description": "Conflito na atualização"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def atualizar_atualizacao_bi(
    request: Request,
    background_tasks: BackgroundTasks,
    bi_id: int,
    bi_data: str = Form(...),
    files: List[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Atualiza um pedido de atualização de BI existente.
    
    - **bi_id**: ID do pedido de atualização
    - **bi_data**: Dados atualizados em formato JSON
    - **files**: Novos documentos de suporte (opcional)
    """
    try:
        logger.info(f"Updating BI update {bi_id} for user {current_user.id}")
        
        # Parse the update data
        try:
            update_data = json.loads(bi_data)
            bi_update = AtualizacaoBIUpdate(**update_data)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados inválidos. Certifique-se de que os dados estão em formato JSON válido."
            )
        
        # Handle file uploads if any
        uploaded_docs = []
        if files:
            for file in files:
                if file.content_type not in ALLOWED_FILE_TYPES:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Tipo de ficheiro não suportado: {file.content_type}"
                    )
                
                if file.size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Ficheiro {file.filename} excede o tamanho máximo de 10MB"
                    )
                
                # Generate a unique filename
                file_ext = ALLOWED_FILE_TYPES[file.content_type]
                filename = f"docs/{uuid.uuid4()}.{file_ext}"
                
                # Save the file
                await save_uploaded_file(file, filename)
                uploaded_docs.append(filename)
        
        # Get the current BI update to check permissions
        current_bi = await get_bi_update_by_id(
            bi_id=bi_id,
            user_id=current_user.id,
            user_role=current_user.role,
            db=db
        )
        
        if not current_bi:
            logger.warning(f"BI update {bi_id} not found or access denied for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido de atualização não encontrado ou acesso negado"
            )
        
        # Check if status transition is allowed
        if hasattr(bi_update, 'status') and bi_update.status != current_bi.status:
            allowed_statuses = get_allowed_status_transitions(
                current_status=current_bi.status,
                user_role=current_user.role
            )
            if bi_update.status not in allowed_statuses:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Transição de estado não permitida de {current_bi.status} para {bi_update.status}"
                )
        
        # Update the BI request
        updated_bi = AtualizacaoBIService.update_bi_request(
            db=db,
            bi_id=bi_id,
            bi_update=bi_update,
            current_user_id=current_user.id,
            background_tasks=background_tasks,
            current_user_role=current_user.role,
            uploaded_docs=uploaded_docs
        )
        
        # Add background tasks if status changed
        if hasattr(bi_update, 'status') and bi_update.status != current_bi.status:
            background_tasks.add_task(
                send_bi_update_notification,
                bi_id=bi_id,
                notification_type=f"status_changed_{bi_update.status}",
                recipient_email=current_user.email,
                previous_status=current_bi.status,
                new_status=bi_update.status
            )
            
            # Additional processing for specific status changes
            if bi_update.status == "em_analise":
                background_tasks.add_task(
                    process_bi_update_analysis,
                    bi_id=bi_id
                )
            elif bi_update.status == "aprovado":
                background_tasks.add_task(
                    generate_bi_document,
                    bi_id=bi_id
                )
        
        logger.info(f"Successfully updated BI update {bi_id} for user {current_user.id}")
        return updated_bi
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating BI update {bi_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao atualizar o pedido"
        )

@router.delete(
    "/{bi_id}",
    status_code=status.HTTP_200_OK,
    summary="Cancelar ou eliminar um pedido de atualização",
    description="Permite ao utilizador cancelar o próprio pedido ou a um administrador eliminar qualquer pedido.",
    responses={
        200: {"description": "Pedido cancelado/eliminado com sucesso"},
        400: {"description": "Pedido não pode ser cancelado no estado atual"},
        401: {"description": "Não autorizado"},
        403: {"description": "Acesso negado"},
        404: {"description": "Pedido não encontrado"},
        500: {"description": "Erro interno do servidor"}
    }
)
async def cancelar_atualizacao_bi(
    request: Request,
    background_tasks: BackgroundTasks,
    bi_id: int,
    razao: Optional[str] = Query(None, description="Razão do cancelamento"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancela um pedido de atualização de BI existente.
    
    - **bi_id**: ID do pedido de atualização a cancelar
    - **razao**: Razão opcional para o cancelamento
    """
    try:
        logger.info(f"Canceling BI update {bi_id} for user {current_user.id}")
        
        # Get the current BI update to check permissions and status
        current_bi = await get_bi_update_by_id(
            bi_id=bi_id,
            user_id=current_user.id,
            user_role=current_user.role,
            db=db
        )
        
        if not current_bi:
            logger.warning(f"BI update {bi_id} not found or access denied for user {current_user.id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido de atualização não encontrado ou acesso negado"
            )
        
        # Check if the request can be canceled
        cancellable_statuses = ["pendente", "rascunho", "em_analise"]
        if current_bi.status not in cancellable_statuses and current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Pedidos no estado '{current_bi.status}' não podem ser cancelados"
            )
        
        # For admin, allow hard deletion if the status allows
        if current_user.role == "admin" and current_bi.status in ["rascunho", "cancelado"]:
            logger.info(f"Admin {current_user.id} is deleting BI update {bi_id}")
            # Delete the BI update request
            AtualizacaoBIService.delete_bi_request(
                db=db,
                bi_id=bi_id,
                current_user_id=current_user.id
            )
            
            # Log the deletion
            logger.info(f"BI update {bi_id} deleted by admin {current_user.id}")
            return {"message": "Pedido eliminado com sucesso"}
        
        # For regular users or non-deletable status, mark as canceled
        await update_bi_update_request(
            bi_id=bi_id,
            bi_update=AtualizacaoBIUpdate(
                status="cancelado",
                motivo_cancelamento=razao or "Solicitado pelo utilizador"
            ),
            user_id=current_user.id,
            user_role=current_user.role,
            db=db
        )
        
        # Add background task for notification
        background_tasks.add_task(
            send_bi_update_notification,
            bi_id=bi_id,
            notification_type="request_canceled",
            recipient_email=current_user.email,
            cancellation_reason=razao
        )
        
        logger.info(f"Successfully canceled BI update {bi_id} for user {current_user.id}")
        return {"message": "Pedido cancelado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error canceling BI update {bi_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro ao processar o cancelamento do pedido"
        )

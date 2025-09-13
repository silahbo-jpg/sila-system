from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.urbanism_alvara_funcionamento import AlvaraFuncionamento
from app.schemas.alvara_funcionamento import (
    AlvaraFuncionamentoCreate, 
    AlvaraFuncionamentoRead, 
    AlvaraFuncionamentoUpdate,
    AlvaraFuncionamento as AlvaraFuncionamentoSchema
)
from app.core.auth.auth_utils import get_current_active_user

router = APIRouter(prefix="/api/alvara-funcionamento", tags=["Alvará de Funcionamento"])

@router.post("/", response_model=AlvaraFuncionamentoRead, status_code=status.HTTP_201_CREATED)
async def criar_alvara_funcionamento(
    data: AlvaraFuncionamentoCreate, 
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create new Operating Permit / Criar novo Alvará de Funcionamento
    
    Args:
        data: Data for creating a new operating permit
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        AlvaraFuncionamentoRead: The created operating permit
    """
    if current_user.get("role") not in ["admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to create operating permits"
        )
    
    try:
        # Create new AlvaraFuncionamento instance
        db_item = AlvaraFuncionamento(
            **data.dict(),
            municipe_id=current_user["id"],
            status="pendente",
            data_criacao=datetime.utcnow(),
            ativo=True
        )
        
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        
        return db_item
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating operating permit: {str(e)}"
        )

@router.get("/{item_id}", response_model=AlvaraFuncionamentoRead)
async def obter_alvara_funcionamento(
    item_id: int, 
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get Operating Permit by ID / Obter Alvará de Funcionamento por ID
    
    Args:
        item_id: ID of the operating permit to retrieve
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        AlvaraFuncionamentoRead: The requested operating permit
    """
    result = await db.execute(
        select(AlvaraFuncionamento).where(AlvaraFuncionamento.id == item_id)
    )
    db_item = result.scalars().first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Operating permit not found"
        )
        
    # Check if user has permission to access this item
    if db_item.municipe_id != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )
        
    return db_item

@router.get("/", response_model=List[AlvaraFuncionamentoRead])
async def listar_alvara_funcionamento(
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    List Operating Permits / Listar Alvarás de Funcionamento
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        status: Optional status filter
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        List[AlvaraFuncionamentoRead]: List of operating permits
    """
    query = select(AlvaraFuncionamento)
    
    # Apply filters based on user role
    if current_user.get("role") != "admin":
        query = query.where(AlvaraFuncionamento.municipe_id == current_user["id"])
    
    # Apply status filter if provided
    if status:
        query = query.where(AlvaraFuncionamento.status == status)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    items = result.scalars().all()
    
    return items

@router.put("/{item_id}", response_model=AlvaraFuncionamentoRead)
async def atualizar_alvara_funcionamento(
    item_id: int, 
    data: AlvaraFuncionamentoUpdate, 
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update Operating Permit / Atualizar Alvará de Funcionamento
    
    Args:
        item_id: ID of the operating permit to update
        data: Data to update
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        AlvaraFuncionamentoRead: The updated operating permit
    """
    # Get the existing item
    result = await db.execute(
        select(AlvaraFuncionamento).where(AlvaraFuncionamento.id == item_id)
    )
    db_item = result.scalars().first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operating permit not found"
        )
    
    # Check permissions
    if db_item.municipe_id != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resource"
        )
    
    try:
        # Update item with new data
        update_data = data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.data_atualizacao = datetime.utcnow()
        
        await db.commit()
        await db.refresh(db_item)
        
        return db_item
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating operating permit: {str(e)}"
        )

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def excluir_alvara_funcionamento(
    item_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete Operating Permit / Excluir Alvará de Funcionamento
    
    Args:
        item_id: ID of the operating permit to delete
        current_user: Currently authenticated user
        db: Database session
    """
    # Get the existing item
    result = await db.execute(
        select(AlvaraFuncionamento).where(AlvaraFuncionamento.id == item_id)
    )
    db_item = result.scalars().first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operating permit not found"
        )
    
    # Check permissions
    if db_item.municipe_id != current_user["id"] and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resource"
        )
    
    try:
        # Soft delete by setting ativo=False
        db_item.ativo = False
        db_item.data_remocao = datetime.utcnow()
        
        await db.commit()
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting operating permit: {str(e)}"
        )
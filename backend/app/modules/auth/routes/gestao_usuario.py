from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.modules.auth.models.gestao_usuario import GestaoUsuario
from app.modules.auth.schemas.gestao_usuario import GestaoUsuarioCreate, GestaoUsuarioRead, GestaoUsuarioUpdate

router = APIRouter(prefix="/internal/gestao-usuario", tags=["Gestão de Usuários"])

@router.post("/", response_model=GestaoUsuarioRead)
def criar_gestao_usuario(data: GestaoUsuarioCreate):
    """Create new User Management / Criar novo Gestão de Usuários"""
    db_item = GestaoUsuario(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/id", response_model=GestaoUsuarioRead)
def obter_gestao_usuario(item_id: int):
    """Get User Management by ID / Obter Gestão de Usuários por ID"""
    item = db.query(GestaoUsuario).filter(GestaoUsuario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gestão de Usuários não encontrado")
    return item

@router.get("/", response_model=List[GestaoUsuarioRead])
def listar_gestao_usuario(skip: int = 0, limit: int = 100):
    """List User Management / Listar Gestão de Usuários"""
    return db.query(GestaoUsuario).offset(skip).limit(limit).all()

@router.put("/id", response_model=GestaoUsuarioRead)
def atualizar_gestao_usuario(item_id: int, data: GestaoUsuarioUpdate):
    """Update User Management / Atualizar Gestão de Usuários"""
    item = db.query(GestaoUsuario).filter(GestaoUsuario.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Gestão de Usuários não encontrado")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

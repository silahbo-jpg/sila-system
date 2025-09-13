from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from datetime import datetime

from app.db import get_db
from app.core.security import get_current_active_user
from app.modules.integration.schemas import EventResponse, EventFilter, EventCreate
from app.modules.integration.services import EventService

router = APIRouter()

@router.post("/events", response_model=EventResponse, status_code=201)
async def create_event(
    event_data: dict = Body(...),
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Cria um novo evento de integração."""
    try:
        # Extrair dados do evento
        event_type = event_data.get("event_type")
        payload = event_data.get("payload", {})
        source_module = event_data.get("source_module")
        
        if not event_type or not source_module:
            raise HTTPException(status_code=400, detail="Tipo de evento e módulo de origem são obrigatórios")
        
        # Publicar o evento
        event = await EventService.publish_event(
            db=db,
            event_type=event_type,
            payload=payload,
            source_module=source_module
        )
        
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao publicar evento: {str(e)}")

@router.get("/events", response_model=List[EventResponse])
async def get_events(
    event_type: Optional[str] = Query(None, description="Filtrar por tipo de evento"),
    source_module: Optional[str] = Query(None, description="Filtrar por módulo de origem"),
    start_date: Optional[datetime] = Query(None, description="Data de início (formato ISO)"),
    end_date: Optional[datetime] = Query(None, description="Data de fim (formato ISO)"),
    limit: int = Query(100, description="Limite de resultados"),
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtém eventos de integração com filtros opcionais."""
    filters = EventFilter(
        event_type=event_type,
        source_module=source_module,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    
    events = EventService.get_events(db=db, filters=filters)
    return events

@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtém um evento específico pelo ID."""
    event = EventService.get_event_by_id(db=db, event_id=event_id)
    
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
        
    return event

@router.get("/events/module/{module_name}", response_model=List[EventResponse])
async def get_events_by_module(
    module_name: str,
    limit: int = Query(50, description="Limite de resultados"),
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtém eventos de um módulo específico."""
    filters = EventFilter(
        source_module=module_name,
        limit=limit
    )
    
    events = EventService.get_events(db=db, filters=filters)
    return events

@router.get("/events/type/{event_type}", response_model=List[EventResponse])
async def get_events_by_type(
    event_type: str,
    limit: int = Query(50, description="Limite de resultados"),
    db = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Obtém eventos de um tipo específico."""
    filters = EventFilter(
        event_type=event_type,
        limit=limit
    )
    
    events = EventService.get_events(db=db, filters=filters)
    return events
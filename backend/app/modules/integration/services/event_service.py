from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import json

from app.modules.integration.models import IntegrationEvent
from app.modules.integration.schemas import EventCreate, EventResponse, EventFilter
from app.modules.integration.integration_gateway import integration_gateway

class EventService:
    """Serviço para gerenciar eventos de integração."""
    
    @staticmethod
    async def publish_event(db: Session, event_type: str, payload: Dict[str, Any], 
                          source_module: str) -> EventResponse:
        """Publica um novo evento no sistema.
        
        Args:
            db: Sessão do banco de dados
            event_type: Tipo de evento
            payload: Dados do evento
            source_module: Módulo que está publicando o evento
            
        Returns:
            O evento criado
        """
        event = await integration_gateway.publish(
            event_type=event_type,
            payload=payload,
            source_module=source_module,
            db=db
        )
        
        return EventResponse(
            id=event.id,
            event_type=event.event_type,
            payload=json.loads(event.payload),
            source_module=event.source_module,
            timestamp=event.timestamp
        )
    
    @staticmethod
    def get_events(db: Session, filters: EventFilter) -> List[EventResponse]:
        """Obtém eventos com base em filtros.
        
        Args:
            db: Sessão do banco de dados
            filters: Filtros para os eventos
            
        Returns:
            Lista de eventos
        """
        query = db.query(IntegrationEvent)
        
        if filters.event_type:
            query = query.filter(IntegrationEvent.event_type == filters.event_type)
            
        if filters.source_module:
            query = query.filter(IntegrationEvent.source_module == filters.source_module)
            
        if filters.start_date:
            query = query.filter(IntegrationEvent.timestamp >= filters.start_date)
            
        if filters.end_date:
            query = query.filter(IntegrationEvent.timestamp <= filters.end_date)
            
        events = query.order_by(IntegrationEvent.timestamp.desc()).limit(filters.limit).all()
        
        return [
            EventResponse(
                id=event.id,
                event_type=event.event_type,
                payload=json.loads(event.payload),
                source_module=event.source_module,
                timestamp=event.timestamp
            ) for event in events
        ]
    
    @staticmethod
    def get_event_by_id(db: Session, event_id: int) -> Optional[EventResponse]:
        """Obtém um evento pelo ID.
        
        Args:
            db: Sessão do banco de dados
            event_id: ID do evento
            
        Returns:
            O evento ou None se não encontrado
        """
        event = db.query(IntegrationEvent).filter(IntegrationEvent.id == event_id).first()
        
        if not event:
            return None
            
        return EventResponse(
            id=event.id,
            event_type=event.event_type,
            payload=json.loads(event.payload),
            source_module=event.source_module,
            timestamp=event.timestamp
        )


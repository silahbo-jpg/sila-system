from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EventBase(BaseModel):
    """Esquema base para eventos de integração."""
    event_type: str
    payload: Dict[str, Any]
    source_module: str

class EventCreate(EventBase):
    """Esquema para criação de eventos de integração."""
    timestamp: datetime

class EventResponse(EventBase):
    """Esquema para resposta de eventos de integração."""
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)

class EventFilter(BaseModel):
    """Esquema para filtrar eventos de integração."""
    event_type: Optional[str] = None
    source_module: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = 100


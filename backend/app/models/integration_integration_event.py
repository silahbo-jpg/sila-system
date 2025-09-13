from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.db.base import Base

class IntegrationEvent(Base):
    """Modelo para eventos de integração entre módulos."""
    __tablename__ = "integration_events"

    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    payload = Column(Text, nullable=False)  # JSON serializado
    source_module = Column(String(50), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)


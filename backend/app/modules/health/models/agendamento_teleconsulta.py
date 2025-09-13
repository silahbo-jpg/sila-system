from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class AgendamentoTeleconsulta(Base):
    __tablename__ = "health_agendamento_teleconsulta"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(String(500))
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    municipe_id = Column(Integer, nullable=False)  # Relaciona com registry


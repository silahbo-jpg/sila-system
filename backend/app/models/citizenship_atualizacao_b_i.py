from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from app.db.base import Base


class AtualizacaoBI(Base):
    __tablename__ = "citizenship_atualizacao_b_i"
    __table_args__ = {"extend_existing": True}  # garante que não haja conflito em testes/imports

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    nome_en = Column(String(200), nullable=False)  # English name
    descricao = Column(String(500), nullable=True)
    descricao_en = Column(String(500), nullable=True)  # English description
    ativo = Column(Boolean, default=True, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    dados_adicionais = Column(JSON, nullable=True)  # dados flexíveis adicionais
    municipe_id = Column(Integer, nullable=False, index=True)  # referência ao cidadão
    status = Column(String(50), default="pendente", nullable=False)

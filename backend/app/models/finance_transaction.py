from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Transaction(Base):
    """Modelo para transações financeiras no sistema SILA.
    
    Este modelo armazena informações detalhadas sobre transações bancárias
    relacionadas aos pagamentos processados pelo sistema.
    """
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    transaction_id = Column(String(100), unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    source_account = Column(String(50), nullable=False)
    destination_account = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)  # PENDING, COMPLETED, FAILED, REFUNDED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    details = Column(JSON, nullable=True)  # Detalhes da transação retornados pelo banco
    
    # Relacionamentos
    payment = relationship("Payment", back_populates="transactions")
    
    def __repr__(self):
        return f"<Transaction {self.transaction_id} - {self.amount} ({self.status})>"


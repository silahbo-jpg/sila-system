from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Payment(Base):
    """Modelo para registros de pagamentos no sistema SILA.
    
    Este modelo armazena informações sobre pagamentos de taxas, multas e
    outros serviços financeiros oferecidos pela administração municipal.
    """
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_type = Column(String(50), nullable=False)  # TAXA, MULTA, LICENCA, etc.
    description = Column(String(255), nullable=False)
    reference_id = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(String(20), nullable=False)  # PENDING, COMPLETED, FAILED, REFUNDED
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    transaction_id = Column(String(100), nullable=True)
    error_message = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)  # Metadados adicionais do pagamento
    
    # Relacionamentos
    postgres = relationship("postgres", back_populates="payments")
    transactions = relationship("Transaction", back_populates="payment")
    
    def __repr__(self):
        return f"<Payment {self.reference_id} - {self.amount} ({self.status})>"


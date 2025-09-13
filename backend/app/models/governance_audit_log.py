from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class AuditLog(Base):
    """Modelo para registro de auditoria de ações no sistema SILA.
    
    Este modelo registra todas as operações críticas realizadas no sistema,
    permitindo rastreabilidade completa para fins de governança e compliance.
    """
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource_type = Column(String(100), nullable=False)  # Nome da tabela/recurso afetado
    resource_id = Column(String(50), nullable=False)  # ID do recurso afetado
    details = Column(JSON, nullable=True)  # Detalhes da operação em formato JSON
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    
    # Relacionamentos
    postgres = relationship("postgres", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.action} on {self.resource_type}:{self.resource_id} by postgres:{self.user_id}>"
    
    @classmethod
    def log_action(cls, db_session, user_id, action, resource_type, resource_id, details=None, ip_address=None, user_agent=None):
        """Método de classe para facilitar o registro de ações de auditoria."""
        audit_entry = cls(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db_session.add(audit_entry)
        db_session.commit()
        return audit_entry


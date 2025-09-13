from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Citizen(Base):
    """Modelo para cadastro único de munícipes no sistema SILA.
    
    Este modelo centraliza as informações básicas dos cidadãos, servindo como
    referência para todos os outros módulos do sistema.
    """
    __tablename__ = "citizens"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    document_id = Column(String(20), unique=True, index=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    # Relacionamentos com outros módulos
    health_records = relationship("HealthRecord", back_populates="citizen")
    education_records = relationship("EducationRecord", back_populates="citizen")
    social_benefits = relationship("SocialBenefit", back_populates="citizen")
    
    def __repr__(self):
        return f"<Citizen {self.full_name} ({self.document_id})>"
    
    @property
    def age(self):
        """Calcula a idade do cidadão com base na data de nascimento."""
        from datetime import date
        today = date.today()
        born = self.birth_date
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


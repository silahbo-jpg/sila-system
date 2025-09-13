"""Módulo de Reclamações (Complaints)

Este módulo fornece funcionalidades para gerenciar reclamações, incluindo:
- Criação e gerenciamento de reclamações
- Categorização de reclamações
- Comentários em reclamações
- Estatísticas e relatórios
"""

from .services import ComplaintService
from .crud import ComplaintCRUD
from .models import (
    ComplaintCreate, ComplaintUpdate, ComplaintResponse,
    ComplaintCommentCreate, ComplaintCommentResponse,
    ComplaintCategoryCreate, ComplaintCategoryUpdate, ComplaintCategoryResponse,
    ComplaintFilter, ComplaintStats
)

__all__ = [
    "ComplaintService", "ComplaintCRUD", "models", "schemas", "crud", 
    "services", "endpoints", "ComplaintCreate", "ComplaintUpdate", 
    "ComplaintResponse", "ComplaintCommentCreate", "ComplaintCommentResponse",
    "ComplaintCategoryCreate", "ComplaintCategoryUpdate", "ComplaintCategoryResponse",
    "ComplaintFilter", "ComplaintStats"
]


# Serviço: Denúncia Cidadã / Citizen Report

# Serviço: Ouvidoria Municipal / Municipal Ombudsman

# Serviço: Reclamação de Serviço / Service Complaint

# Serviço: Sugestão de Melhoria / Improvement Suggestion

# Serviço: Fiscalização de Obra / Construction Oversight

# Serviço: Denúncia Ambiental / Environmental Report

# Serviço: Violação de Direitos / Rights Violation

# Serviço: Corrupção Administrativa / Administrative Corruption

# Serviço: Mau Atendimento / Poor Service

# Serviço: Irregularidade Fiscal / Tax Irregularity

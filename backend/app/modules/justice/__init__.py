"""Justice module.

This module provides functionality for judicial services including certificate generation
and management for various legal documents.
"""

from . import models, schemas, crud, services, routes
from .models import *
from .schemas import *
from .crud import *

__all__ = [
    "models",
    "schemas",
    "crud",
    "services",
    "routes",
    # Enums
    "CertificateType",
    "CertificateStatus",
    # Base schemas
    "JudicialCertificateBase",
    # CRUD operations
    "create_certificate",
    "get_certificate",
    "get_certificates",
    "update_certificate",
    "delete_certificate",
]

# Service: Mediação de Conflitos / Conflict Mediation
# Service: Assistência Jurídica Gratuita / Free Legal Assistance
# Service: Registo Criminal / Criminal Record
# Service: Habeas Corpus / Habeas Corpus
# Service: Mandado de Segurança / Security Order

# Serviço: Defensor Público / Public Defender

# Serviço: Cartório Distribuidor / Distribution Office

# Serviço: Execução Fiscal / Tax Execution

# Serviço: Penhora de Bens / Asset Seizure

# Serviço: Leilão Judicial / Judicial Auction

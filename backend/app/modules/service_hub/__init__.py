# Service Hub Module
# Sistema Integrado Local de Administração (SILA)

"""
Módulo de Catálogo de Serviços (Service Hub)

Este módulo é responsável por gerenciar o catálogo de serviços disponíveis no SILA,
permitindo que qualquer departamento registre seus serviços na plataforma.
"""

from fastapi import APIRouter

# Import the main endpoints router instead of individual route files
from app.modules.service_hub.endpoints import router as service_hub_router

router = APIRouter()
router.include_router(service_hub_router)

# Serviço: Jornada Cidadã / Citizen Journey

# Serviço: Portal Único de Serviços / Single Service Portal

# Serviço: Atendimento Integrado / Integrated Service

# Serviço: Agendamento Unificado / Unified Scheduling

# Serviço: Status de Solicitação / Request Status

# Serviço: Notificação ao Cidadão / Citizen Notification

# Serviço: Canal de Comunicação / Communication Channel

# Serviço: Suporte Técnico / Technical Support

# Serviço: Tutorial de Serviço / Service Tutorial

# Serviço: Avaliação de Serviço / Service Evaluation

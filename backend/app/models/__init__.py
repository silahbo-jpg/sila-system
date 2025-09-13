"""
This module imports all SQLAlchemy models to ensure they are registered with the SQLAlchemy metadata.
Importing this module will make all models available through SQLAlchemy's metadata.
"""

# Import models explicitly to avoid circular imports
# The order of imports matters if there are foreign key relationships between models

# Registry models
from .registry_citizen import Citizen  # noqa: F401

# Citizenship models
from .citizenship_atualizacao_b_i import AtualizacaoBI  # noqa: F401
from .citizenship_emissao_b_i import EmissaoBI  # noqa: F401
from .citizenship_emissao_passaporte import EmissaoPassaporte  # noqa: F401

# Add other model imports as needed, grouping them by domain
from . import registry_tutela_menor
from . import sanitation_agente_sanitario
from . import sanitation_controle_vetores
from . import sanitation_educacao_ambiental
from . import sanitation_esgoto_sanitario
from . import sanitation_limpeza_urbana
from . import sanitation_monitoramento_ambiental
from . import sanitation_tratamento_agua
from . import social_assistencia_mulher
from . import social_auxilio_social
from . import social_bolsa_familia
from . import social_capacitacao_profissional
from . import social_habitacao_social
from . import social_inclusao_digital
from . import social_programa_idoso
from . import social_protecao_menor
from . import social_reabilitacao_social
from . import social_seguranca_alimentar
from . import statistics_analise_dados
from . import statistics_dashboard_executivo
from . import statistics_metricas_uso
from . import statistics_relatorio_k_p_i
from . import urbanism_alvara_funcionamento
from . import urbanism_demolicao_edificio
from . import urbanism_espaco_publico
from . import urbanism_inspecao_obra
from . import urbanism_licenca_construcao
from . import urbanism_loteamento_urbano
from . import urbanism_ocupacao_solo
from . import urbanism_plano_urbano
from . import urbanism_regularizacao_fundiaria
from . import urbanism_sinalizacao_trafego

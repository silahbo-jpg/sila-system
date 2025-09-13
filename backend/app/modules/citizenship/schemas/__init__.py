# This file makes the schemas directory a Python package
# Import all schema modules here for easier access
from .atualizacao_b_i import AtualizacaoBICreate, AtualizacaoBIRead, AtualizacaoBIUpdate

__all__ = [
    'AtualizacaoBICreate',
    'AtualizacaoBIRead',
    'AtualizacaoBIUpdate',
]

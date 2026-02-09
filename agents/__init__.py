"""
Package agents pour le projet scraper
"""

from .agent_universel import (
    Produit,
    AgentProduitUniversel,
    analyser_produits
)

__all__ = [
    'Produit',
    'AgentProduitUniversel',
    'analyser_produits'
]

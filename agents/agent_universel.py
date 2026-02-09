"""
AGENT UNIVERSEL POUR TOUS LES PRODUITS
=======================================

Cet agent fonctionne avec N'IMPORTE QUEL TYPE DE PRODUIT :
- Micro-ondes, smartphones, ordinateurs, vêtements, etc.
- Flexible et personnalisable
- Système de scoring adaptatif

Auteur : Claude
Date : 2026-02-08
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
from datetime import datetime


# ============================================================================
# CLASSES DE DONNÉES
# ============================================================================

@dataclass
class Produit:
    """
    Classe universelle pour représenter N'IMPORTE QUEL produit
    
    Attributs obligatoires :
        nom: Nom du produit
        marque: Marque
        prix: Prix en euros
    
    Attributs optionnels (adaptez selon vos besoins) :
        note: Note utilisateurs (sur 5)
        nb_avis: Nombre d'avis
        caracteristiques: Liste de caractéristiques
        url: Lien vers le produit
        source: D'où vient le produit
        image_url: URL de l'image
        stock: Disponibilité
        ... ajoutez ce que vous voulez !
    """
    # Obligatoires
    nom: str
    marque: str
    prix: float
    
    # Optionnels (avec valeurs par défaut)
    note: float = 4.0
    nb_avis: int = 0
    caracteristiques: List[str] = field(default_factory=list)
    url: str = ""
    source: str = ""
    image_url: str = ""
    stock: bool = True
    
    # Métadonnées (automatiques)
    date_ajout: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Attributs personnalisés (dict flexible)
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculer le score automatiquement à la création"""
        self._score = self._calculer_score()
    
    @property
    def score_qualite_prix(self) -> float:
        """Score qualité/prix calculé automatiquement"""
        return self._score
    
    def _calculer_score(self) -> float:
        """
        Calcule un score de 0 à 100
        
        Système de scoring adaptatif :
        - 40% : Note utilisateurs
        - 30% : Prix (bonus si raisonnable)
        - 20% : Nombre d'avis (popularité)
        - 10% : Bonus caractéristiques
        
        PERSONNALISABLE : Modifiez les poids selon vos besoins !
        """
        score = 0
        
        # 1. Score basé sur note (40 points max)
        if self.note > 0:
            score += (self.note / 5) * 40
        
        # 2. Score basé sur prix (30 points max)
        # Plus le prix est bas (par rapport à 500€), meilleur c'est
        # Adaptez le seuil selon votre type de produit !
        prix_reference = self.extra.get('prix_reference', 500)
        if self.prix > 0:
            ratio_prix = max(0, 1 - (self.prix / prix_reference))
            score += ratio_prix * 30
        
        # 3. Score basé sur nombre d'avis (20 points max)
        if self.nb_avis >= 200:
            score += 20
        elif self.nb_avis >= 100:
            score += 15
        elif self.nb_avis >= 50:
            score += 10
        elif self.nb_avis >= 10:
            score += 5
        
        # 4. Bonus caractéristiques (10 points max)
        nb_caracteristiques = len(self.caracteristiques)
        score += min(nb_caracteristiques * 2, 10)
        
        return min(score, 100)  # Plafonner à 100
    
    @property
    def categorie_prix(self) -> str:
        """Catégoriser le prix (adaptable)"""
        if self.prix < 50:
            return "💰 Entrée de gamme"
        elif self.prix < 150:
            return "💵 Milieu de gamme"
        elif self.prix < 300:
            return "💎 Haut de gamme"
        else:
            return "👑 Premium"
    
    def to_dict(self) -> Dict:
        """Convertir en dictionnaire"""
        return {
            'nom': self.nom,
            'marque': self.marque,
            'prix': self.prix,
            'note': self.note,
            'nb_avis': self.nb_avis,
            'score_qualite_prix': self.score_qualite_prix,
            'categorie_prix': self.categorie_prix,
            'caracteristiques': self.caracteristiques,
            'url': self.url,
            'source': self.source,
            'stock': self.stock,
            'extra': self.extra
        }


# ============================================================================
# AGENT UNIVERSEL
# ============================================================================

class AgentProduitUniversel:
    """
    Agent intelligent pour analyser et recommander N'IMPORTE QUEL produit
    
    Utilisation :
        agent = AgentProduitUniversel(type_produit="smartphone")
        agent.ajouter_produit(nom="iPhone 15", marque="Apple", prix=999)
        recommandations = agent.obtenir_recommandations(budget=1000)
    """
    
    def __init__(self, type_produit: str = "produit"):
        """
        Initialiser l'agent
        
        Args:
            type_produit: Type de produit (pour logs et rapports)
        """
        self.type_produit = type_produit
        self.produits: List[Produit] = []
        self.historique_recherches: List[Dict] = []
    
    # ========================================================================
    # MÉTHODES D'AJOUT DE PRODUITS
    # ========================================================================
    
    def ajouter_produit(self, 
                       nom: str, 
                       marque: str, 
                       prix: float,
                       **kwargs) -> Produit:
        """
        Ajouter un produit (méthode simple)
        
        Args:
            nom: Nom du produit
            marque: Marque
            prix: Prix
            **kwargs: Autres attributs (note, nb_avis, etc.)
        
        Returns:
            Le produit créé
        
        Exemple:
            agent.ajouter_produit(
                nom="iPhone 15",
                marque="Apple",
                prix=999,
                note=4.5,
                nb_avis=1500,
                caracteristiques=["5G", "128GB"]
            )
        """
        produit = Produit(nom=nom, marque=marque, prix=prix, **kwargs)
        self.produits.append(produit)
        return produit
    
    def ajouter_produits_depuis_dict(self, produits_data: List[Dict]) -> int:
        """
        Ajouter plusieurs produits depuis une liste de dictionnaires
        
        Args:
            produits_data: Liste de dicts avec infos produits
        
        Returns:
            Nombre de produits ajoutés
        
        Exemple:
            data = [
                {'nom': 'Produit 1', 'marque': 'Samsung', 'prix': 299},
                {'nom': 'Produit 2', 'marque': 'LG', 'prix': 399}
            ]
            agent.ajouter_produits_depuis_dict(data)
        """
        count = 0
        for data in produits_data:
            try:
                self.ajouter_produit(**data)
                count += 1
            except Exception as e:
                print(f"Erreur ajout produit {data.get('nom', '?')}: {e}")
        
        return count
    
    def ajouter_produits_depuis_json(self, fichier_json: str) -> int:
        """
        Charger produits depuis fichier JSON
        
        Args:
            fichier_json: Chemin vers fichier JSON
        
        Returns:
            Nombre de produits chargés
        """
        try:
            with open(fichier_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return self.ajouter_produits_depuis_dict(data)
            elif isinstance(data, dict) and 'produits' in data:
                return self.ajouter_produits_depuis_dict(data['produits'])
            else:
                print("Format JSON non reconnu")
                return 0
        except Exception as e:
            print(f"Erreur lecture JSON: {e}")
            return 0
    
    # ========================================================================
    # MÉTHODES DE FILTRAGE
    # ========================================================================
    
    def filtrer_par_budget(self, budget_max: float) -> List[Produit]:
        """Filtrer produits dans le budget"""
        return [p for p in self.produits if p.prix <= budget_max]
    
    def filtrer_par_marque(self, marques: List[str]) -> List[Produit]:
        """Filtrer par marques"""
        marques_lower = [m.lower() for m in marques]
        return [p for p in self.produits if p.marque.lower() in marques_lower]
    
    def filtrer_par_note(self, note_min: float = 4.0) -> List[Produit]:
        """Filtrer par note minimale"""
        return [p for p in self.produits if p.note >= note_min]
    
    def filtrer_par_caracteristique(self, caracteristique: str) -> List[Produit]:
        """Filtrer par caractéristique"""
        carac_lower = caracteristique.lower()
        return [
            p for p in self.produits 
            if any(carac_lower in c.lower() for c in p.caracteristiques)
        ]
    
    def filtrer_personnalise(self, fonction_filtre) -> List[Produit]:
        """
        Filtrer avec fonction personnalisée
        
        Exemple:
            # Produits Samsung avec note > 4.5
            results = agent.filtrer_personnalise(
                lambda p: p.marque == "Samsung" and p.note > 4.5
            )
        """
        return [p for p in self.produits if fonction_filtre(p)]
    
    # ========================================================================
    # MÉTHODES D'ANALYSE
    # ========================================================================
    
    def obtenir_top(self, 
                    n: int = 3, 
                    budget_max: Optional[float] = None,
                    critere: str = 'score') -> List[Produit]:
        """
        Obtenir le top N des produits
        
        Args:
            n: Nombre de produits à retourner
            budget_max: Budget maximum (optionnel)
            critere: 'score', 'prix', 'note', 'popularite'
        
        Returns:
            Liste des N meilleurs produits
        """
        # Filtrer par budget si spécifié
        produits = self.produits if budget_max is None else self.filtrer_par_budget(budget_max)
        
        # Trier selon critère
        if critere == 'score':
            produits_tries = sorted(produits, key=lambda p: p.score_qualite_prix, reverse=True)
        elif critere == 'prix':
            produits_tries = sorted(produits, key=lambda p: p.prix)
        elif critere == 'note':
            produits_tries = sorted(produits, key=lambda p: p.note, reverse=True)
        elif critere == 'popularite':
            produits_tries = sorted(produits, key=lambda p: p.nb_avis, reverse=True)
        else:
            produits_tries = produits
        
        return produits_tries[:n]
    
    def obtenir_statistiques(self) -> Dict[str, Any]:
        """Obtenir statistiques sur les produits"""
        if not self.produits:
            return {}
        
        prix = [p.prix for p in self.produits]
        notes = [p.note for p in self.produits if p.note > 0]
        scores = [p.score_qualite_prix for p in self.produits]
        
        return {
            'nb_produits': len(self.produits),
            'prix_moyen': sum(prix) / len(prix) if prix else 0,
            'prix_min': min(prix) if prix else 0,
            'prix_max': max(prix) if prix else 0,
            'note_moyenne': sum(notes) / len(notes) if notes else 0,
            'score_moyen': sum(scores) / len(scores) if scores else 0,
            'marques': list(set(p.marque for p in self.produits)),
            'nb_marques': len(set(p.marque for p in self.produits))
        }
    
    # ========================================================================
    # RECOMMANDATIONS
    # ========================================================================
    
    def obtenir_recommandations(self, 
                                budget_max: Optional[float] = None,
                                marques_preferees: Optional[List[str]] = None,
                                note_min: float = 3.5,
                                top_n: int = 3) -> Dict[str, Any]:
        """
        Obtenir recommandations personnalisées
        
        Args:
            budget_max: Budget maximum
            marques_preferees: Liste de marques préférées
            note_min: Note minimale
            top_n: Nombre de recommandations
        
        Returns:
            Dict avec recommandations et analyses
        """
        # Filtrer
        produits = self.produits
        
        if budget_max:
            produits = [p for p in produits if p.prix <= budget_max]
        
        if marques_preferees:
            marques_lower = [m.lower() for m in marques_preferees]
            produits = [p for p in produits if p.marque.lower() in marques_lower]
        
        produits = [p for p in produits if p.note >= note_min]
        
        # Trier par score
        produits_tries = sorted(produits, key=lambda p: p.score_qualite_prix, reverse=True)
        
        # Top N
        top = produits_tries[:top_n]
        
        return {
            'nb_produits_trouves': len(produits),
            'top_recommandations': [p.to_dict() for p in top],
            'meilleur_produit': top[0].to_dict() if top else None,
            'meilleur_prix': min(produits, key=lambda p: p.prix).to_dict() if produits else None,
            'meilleure_note': max(produits, key=lambda p: p.note).to_dict() if produits else None,
            'criteres': {
                'budget_max': budget_max,
                'marques_preferees': marques_preferees,
                'note_min': note_min
            }
        }
    
    # ========================================================================
    # RAPPORTS
    # ========================================================================
    
    def generer_rapport_texte(self, 
                              budget_max: Optional[float] = None,
                              top_n: int = 5) -> str:
        """Générer rapport texte lisible"""
        
        stats = self.obtenir_statistiques()
        top = self.obtenir_top(n=top_n, budget_max=budget_max)
        
        lignes = []
        lignes.append("=" * 80)
        lignes.append(f"📊 RAPPORT D'ANALYSE - {self.type_produit.upper()}")
        lignes.append("=" * 80)
        lignes.append(f"\n📅 Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        lignes.append(f"📦 Produits analysés : {stats.get('nb_produits', 0)}")
        
        if budget_max:
            lignes.append(f"💰 Budget max : {budget_max}€")
            produits_budget = self.filtrer_par_budget(budget_max)
            lignes.append(f"✅ Dans le budget : {len(produits_budget)}")
        
        lignes.append(f"\n💵 Prix moyen : {stats.get('prix_moyen', 0):.2f}€")
        lignes.append(f"📊 Prix min-max : {stats.get('prix_min', 0):.2f}€ - {stats.get('prix_max', 0):.2f}€")
        lignes.append(f"⭐ Note moyenne : {stats.get('note_moyenne', 0):.1f}/5")
        lignes.append(f"🏢 Marques : {stats.get('nb_marques', 0)}")
        
        lignes.append(f"\n{'=' * 80}")
        lignes.append(f"🏆 TOP {len(top)} - MEILLEUR RAPPORT QUALITÉ/PRIX")
        lignes.append("=" * 80)
        
        for i, produit in enumerate(top, 1):
            lignes.append(f"\n{i}. {produit.marque} {produit.nom}")
            lignes.append(f"   {produit.categorie_prix} - {produit.prix}€")
            lignes.append(f"   🎯 Score Q/P : {produit.score_qualite_prix:.1f}/100")
            lignes.append(f"   ⭐ {produit.note}/5 ({produit.nb_avis} avis)")
            if produit.caracteristiques:
                lignes.append(f"   ✨ {', '.join(produit.caracteristiques[:3])}")
        
        lignes.append(f"\n{'=' * 80}")
        lignes.append(f"💡 RECOMMANDATION")
        lignes.append("=" * 80)
        
        if top:
            meilleur = top[0]
            lignes.append(f"\n🎯 Choix optimal : {meilleur.marque} {meilleur.nom}")
            lignes.append(f"   Prix : {meilleur.prix}€ | Score : {meilleur.score_qualite_prix:.1f}/100")
            lignes.append(f"   Note : {meilleur.note}/5 ⭐")
        
        lignes.append(f"\n{'=' * 80}\n")
        
        return "\n".join(lignes)
    
    def exporter_json(self, fichier: str, budget_max: Optional[float] = None):
        """Exporter résultats en JSON"""
        top = self.obtenir_top(budget_max=budget_max, n=10)
        stats = self.obtenir_statistiques()
        
        data = {
            'metadata': {
                'type_produit': self.type_produit,
                'date': datetime.now().isoformat(),
                'budget_max': budget_max
            },
            'statistiques': stats,
            'top_produits': [p.to_dict() for p in top],
            'tous_produits': [p.to_dict() for p in self.produits]
        }
        
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Résultats exportés : {fichier}")
    
    def vider(self):
        """Vider la liste des produits"""
        self.produits = []
    
    def __len__(self):
        """Nombre de produits"""
        return len(self.produits)
    
    def __repr__(self):
        return f"<AgentProduitUniversel({self.type_produit}): {len(self.produits)} produits>"


# ============================================================================
# FONCTION HELPER POUR INTÉGRATION RAPIDE
# ============================================================================

def analyser_produits(produits_data: List[Dict], 
                     budget_max: float,
                     type_produit: str = "produit") -> Dict[str, Any]:
    """
    Fonction ultra-simple pour analyse rapide
    
    Args:
        produits_data: Liste de dicts avec vos produits
        budget_max: Budget maximum
        type_produit: Type de produit
    
    Returns:
        Recommandations complètes
    
    Exemple:
        resultats = analyser_produits(
            produits_data=mes_produits,
            budget_max=500,
            type_produit="smartphone"
        )
        print(resultats['meilleur_produit'])
    """
    agent = AgentProduitUniversel(type_produit)
    agent.ajouter_produits_depuis_dict(produits_data)
    return agent.obtenir_recommandations(budget_max=budget_max)

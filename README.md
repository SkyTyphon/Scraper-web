# 🚀 PROJET SCRAPER COMPLET

Agent universel d'analyse et de recommandation de produits.

---

## 📁 STRUCTURE DU PROJET

```
scraper_project/
├── agents/                      # Agent d'analyse de produits
│   ├── __init__.py
│   └── agent_universel.py      # Agent principal
│
├── data/                        # Données et résultats
│   ├── produits_exemple.json
│   └── resultats_tablettes.json
│
├── docs/                        # Documentation
│   ├── README.md               # Doc complète de l'agent
│   ├── DEMARRAGE_RAPIDE.txt
│   └── GUIDE_INTEGRATION_PAS_A_PAS.md
│
├── main.py                      # Exemples d'utilisation de l'agent
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

---

## 🎯 COMPOSANTS DU PROJET

### 1. **Agent Universel de Produits** (`agents/`)

Agent intelligent pour analyser et recommander des produits :
- Analyse n'importe quel type de produit
- Calcul de score qualité/prix
- Filtrage et recommandations
- Export JSON, rapports texte

**Utilisation rapide :**
```python
from agents import AgentProduitUniversel

agent = AgentProduitUniversel(type_produit="smartphone")
agent.ajouter_produit(nom="iPhone 15", marque="Apple", prix=999)
meilleur = agent.obtenir_top(n=1)[0]
```

**Documentation :** Voir `docs/README.md`

---

## ⚡ DÉMARRAGE RAPIDE

### 1. Tester l'agent :
```bash
python main.py
```
Cela lance 7 exemples complets !

### 2. Utiliser dans votre code :
```python
from agents import analyser_produits

produits = [
    {'nom': 'Produit A', 'marque': 'Samsung', 'prix': 299, 'note': 4.5},
    {'nom': 'Produit B', 'marque': 'LG', 'prix': 399, 'note': 4.7}
]

resultats = analyser_produits(produits, budget_max=500)
print(resultats['meilleur_produit'])
```

---

## 📖 DOCUMENTATION

**Pour commencer :**
1. 📄 `docs/DEMARRAGE_RAPIDE.txt` - Guide ultra-rapide (2 min)
2. 📗 `docs/GUIDE_INTEGRATION_PAS_A_PAS.md` - Intégration détaillée
3. 📘 `docs/README.md` - Documentation complète

**Exemples pratiques :**
- `main.py` - 7 exemples d'utilisation

---

## 💡 CAS D'USAGE

✅ **Web Scraping + Analyse**
- Scraper des sites e-commerce
- Analyser les produits automatiquement
- Obtenir les meilleurs choix

✅ **Comparateur de prix**
- Comparer prix sur plusieurs sites
- Trouver les meilleures offres

✅ **Surveillance de prix**
- Suivre l'évolution des prix
- Alertes sur les baisses

✅ **API de recommandations**
- Créer une API Flask/FastAPI
- Fournir des recommandations

---

## 🔧 INSTALLATION

### Prérequis
- Python 3.7+

```bash
# Aucune dépendance externe requise !
# L'agent utilise uniquement la bibliothèque standard Python
```

---

## 🚀 EXEMPLES RAPIDES

### Exemple 1 : Analyser des produits scrapés
```python
from agents import AgentProduitUniversel
import requests
from bs4 import BeautifulSoup

# 1. Scraper un site
response = requests.get('https://exemple.com')
soup = BeautifulSoup(response.text, 'html.parser')

produits = []
for item in soup.select('.produit'):
    produits.append({
        'nom': item.select_one('.nom').text,
        'prix': float(item.select_one('.prix').text.replace('€', ''))
    })

# 2. Analyser avec l'agent
agent = AgentProduitUniversel(type_produit="produit")
agent.ajouter_produits_depuis_dict(produits)

# 3. Obtenir recommandations
top = agent.obtenir_top(n=3, budget_max=500)
for p in top:
    print(f"{p.marque} {p.nom} - {p.prix}€")
```

### Exemple 2 : Fonction réutilisable
```python
from agents import analyser_produits

def scraper_et_recommander(url, budget):
    # Votre code de scraping
    produits = scraper_site(url)
    
    # Analyse en une ligne !
    resultats = analyser_produits(produits, budget_max=budget)
    
    return resultats['meilleur_produit']
```

---

## 📊 FONCTIONNALITÉS DE L'AGENT

### Analyse et Scoring
- ✅ Score qualité/prix automatique
- ✅ Pondération personnalisable
- ✅ Support de tout type de produit

### Filtrage
- ✅ Par budget
- ✅ Par marque
- ✅ Par note
- ✅ Par caractéristiques
- ✅ Filtres personnalisés

### Export et Rapports
- ✅ Export JSON
- ✅ Rapports texte
- ✅ Statistiques détaillées

---

## 🎨 PERSONNALISATION

### Adapter le scoring
Modifiez `agents/agent_universel.py`, méthode `_calculer_score()` :

```python
def _calculer_score(self) -> float:
    score = 0
    
    # Personnalisez les poids !
    score += (self.note / 5) * 50  # 50% pour la note
    score += ...  # Vos critères
    
    return min(score, 100)
```

---

## 🔗 INTÉGRATION AVEC VOS PROJETS

### Avec Scrapy
```python
from agents import AgentProduitUniversel

class MonSpider(scrapy.Spider):
    def __init__(self):
        self.agent = AgentProduitUniversel(type_produit="produit")
    
    def parse(self, response):
        # Votre code de parsing
        self.agent.ajouter_produit(nom=..., prix=...)
```

### Avec Flask
```python
from flask import Flask, jsonify
from agents import analyser_produits

@app.route('/analyser', methods=['POST'])
def analyser():
    resultats = analyser_produits(
        produits_data=request.json['produits'],
        budget_max=request.json['budget']
    )
    return jsonify(resultats)
```

---

## 🆘 SUPPORT

**Problèmes courants :**

1. **ModuleNotFoundError: No module named 'agents'**
   → Vérifiez que `agents/` est bien dans votre projet

2. **Python < 3.7**
   → Mettez à jour Python (dataclasses requis)

3. **Scores tous identiques**
   → Ajoutez `note` et `nb_avis` à vos produits

**Ressources :**
- Documentation dans `docs/`
- Exemples dans `main.py`
- Code commenté dans `agents/agent_universel.py`

---

## 📝 TODO / AMÉLIORATIONS FUTURES

- [ ] Interface web pour visualiser les résultats
- [ ] Intégration avec plus de sources de données
- [ ] Dashboard en temps réel
- [ ] Support de bases de données (MySQL, PostgreSQL)
- [ ] API REST complète
- [ ] Tests unitaires

---

## 📜 LICENCE

Créé avec ❤️ par Claude | 2026-02-08

Libre d'utilisation pour vos projets personnels et commerciaux !

---

## 🎉 COMMENCER MAINTENANT

```bash
# 1. Tester les exemples
python main.py

# 2. Lire la doc rapide
cat docs/DEMARRAGE_RAPIDE.txt

# 3. Intégrer dans votre projet !
# Voir docs/GUIDE_INTEGRATION_PAS_A_PAS.md
```

**Bon scraping ! 🚀**

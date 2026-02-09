# 🚀 PROJET SCRAPER - AGENT UNIVERSEL

Agent intelligent pour analyser et recommander **N'IMPORTE QUEL TYPE DE PRODUIT**.

---

## 📋 CONTENU DU PROJET

```
scraper/
├── agents/                    # Agent universel
│   ├── __init__.py
│   └── agent_universel.py    # Classe principale
│
├── utils/                     # Utilitaires (scraping, etc.)
├── data/                      # Données JSON
├── config/                    # Configuration
│
├── main.py                    # Exemples d'utilisation
└── README.md                  # Ce fichier
```

---

## ⚡ DÉMARRAGE RAPIDE (30 SECONDES)

### 1. Lancer les exemples

```bash
cd scraper
python main.py
```

Cela lance 7 exemples qui vous montrent toutes les fonctionnalités !

### 2. Utiliser dans votre code

```python
from agents import AgentProduitUniversel

# Créer agent
agent = AgentProduitUniversel(type_produit="smartphone")

# Ajouter produits
agent.ajouter_produit(
    nom="iPhone 15",
    marque="Apple",
    prix=999,
    note=4.7,
    nb_avis=2000
)

# Obtenir recommandations
top = agent.obtenir_top(n=3, budget_max=1000)
print(f"Meilleur : {top[0].marque} {top[0].nom}")
```

---

## 🎯 CAS D'USAGE POUR VOTRE SCRAPER

### Scénario typique :

1. **Vous scrapez** des sites web → obtenir liste de produits
2. **Vous chargez** dans l'agent → analyser les produits
3. **L'agent recommande** → obtenir les meilleurs choix

---

## 📖 GUIDE D'INTÉGRATION DANS VOTRE SCRAPER

### Étape 1 : Scraper vos produits

```python
# Votre code de scraping existant
def scraper_site(url):
    """Votre fonction de scraping"""
    # ... votre code ...
    
    return [
        {
            'nom': 'Produit 1',
            'marque': 'Samsung',
            'prix': 299.99,
            'note': 4.5,
            'nb_avis': 500,
            'url': 'https://...',
            # ... autres infos ...
        },
        # ... autres produits ...
    ]
```

### Étape 2 : Analyser avec l'agent

```python
from agents import AgentProduitUniversel

def analyser_produits_scrapes(produits_scrapes, budget_max):
    """Analyser les produits scrapés"""
    
    # Créer agent
    agent = AgentProduitUniversel(type_produit="votre_type")
    
    # Charger produits scrapés
    agent.ajouter_produits_depuis_dict(produits_scrapes)
    
    # Obtenir recommandations
    recommandations = agent.obtenir_recommandations(
        budget_max=budget_max,
        note_min=4.0,
        top_n=5
    )
    
    return recommandations
```

### Étape 3 : Utiliser

```python
# Dans votre script principal
produits = scraper_site('https://exemple.com')
resultats = analyser_produits_scrapes(produits, budget_max=500)

print(f"Meilleur produit : {resultats['meilleur_produit']}")
```

---

## 🔧 FONCTIONS PRINCIPALES

### 1. Créer un agent

```python
agent = AgentProduitUniversel(type_produit="smartphone")
```

### 2. Ajouter des produits

**Option A : Un par un**
```python
agent.ajouter_produit(
    nom="iPhone 15",
    marque="Apple",
    prix=999,
    note=4.7,
    nb_avis=2000,
    caracteristiques=["5G", "256GB"]
)
```

**Option B : Depuis liste de dicts (RECOMMANDÉ)**
```python
produits = [
    {'nom': 'Produit 1', 'marque': 'Samsung', 'prix': 299},
    {'nom': 'Produit 2', 'marque': 'LG', 'prix': 399}
]
agent.ajouter_produits_depuis_dict(produits)
```

**Option C : Depuis fichier JSON**
```python
agent.ajouter_produits_depuis_json('data/produits.json')
```

### 3. Obtenir recommandations

```python
# Top 3 produits
top_3 = agent.obtenir_top(n=3, budget_max=500)

# Recommandations complètes
recommandations = agent.obtenir_recommandations(
    budget_max=500,
    marques_preferees=['Samsung', 'LG'],
    note_min=4.0,
    top_n=5
)
```

### 4. Filtrer

```python
# Par budget
produits_budget = agent.filtrer_par_budget(500)

# Par marque
produits_samsung = agent.filtrer_par_marque(['Samsung'])

# Par note
produits_notes = agent.filtrer_par_note(4.5)

# Filtre personnalisé
resultats = agent.filtrer_personnalise(
    lambda p: p.marque == 'Apple' and p.prix < 1000
)
```

### 5. Générer rapports

```python
# Rapport texte
rapport = agent.generer_rapport_texte(budget_max=500)
print(rapport)

# Export JSON
agent.exporter_json('resultats.json', budget_max=500)

# Statistiques
stats = agent.obtenir_statistiques()
print(f"Prix moyen : {stats['prix_moyen']:.2f}€")
```

---

## 💡 FONCTION ULTRA-SIMPLE

Si vous voulez juste analyser rapidement :

```python
from agents import analyser_produits

# Vos produits
mes_produits = [
    {'nom': 'Produit A', 'marque': 'Samsung', 'prix': 299, 'note': 4.5},
    {'nom': 'Produit B', 'marque': 'LG', 'prix': 399, 'note': 4.7}
]

# Analyser EN UNE LIGNE
resultats = analyser_produits(
    produits_data=mes_produits,
    budget_max=500,
    type_produit="smartphone"
)

# Utiliser
print(resultats['meilleur_produit'])
```

---

## 🎨 PERSONNALISATION

### Adapter le scoring

Le scoring est dans `agents/agent_universel.py`, méthode `_calculer_score()`.

Par défaut :
- 40% : Note utilisateurs
- 30% : Prix (bonus si raisonnable)
- 20% : Popularité (nombre d'avis)
- 10% : Caractéristiques

**Pour modifier :**

```python
# Dans agent_universel.py, ligne ~90
def _calculer_score(self) -> float:
    score = 0
    
    # Modifier les poids ici !
    score += (self.note / 5) * 50  # 50% au lieu de 40%
    # ... etc
```

### Ajouter attributs personnalisés

```python
agent.ajouter_produit(
    nom="Produit",
    marque="Samsung",
    prix=299,
    # Attributs standards
    note=4.5,
    nb_avis=500,
    # Attributs personnalisés dans 'extra'
    extra={
        'couleur': 'noir',
        'poids': 200,
        'dimensions': '15x10x5',
        'garantie': '2 ans'
    }
)
```

---

## 📊 EXEMPLES CONCRETS

### Exemple 1 : Scraper + Analyser

```python
import requests
from bs4 import BeautifulSoup
from agents import AgentProduitUniversel

def scraper_et_analyser(url, budget):
    """Scraper un site et analyser"""
    
    # 1. Scraper
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    produits = []
    for item in soup.select('.produit'):
        produits.append({
            'nom': item.select_one('.nom').text,
            'marque': item.select_one('.marque').text,
            'prix': float(item.select_one('.prix').text.replace('€', '')),
            'note': float(item.select_one('.note').text),
            'url': item.select_one('a')['href']
        })
    
    # 2. Analyser
    agent = AgentProduitUniversel(type_produit="produit")
    agent.ajouter_produits_depuis_dict(produits)
    
    # 3. Recommander
    top = agent.obtenir_top(n=3, budget_max=budget)
    
    return top

# Utilisation
meilleurs = scraper_et_analyser('https://exemple.com', budget=500)
for p in meilleurs:
    print(f"- {p.marque} {p.nom} : {p.prix}€")
```

### Exemple 2 : Comparateur de prix

```python
from agents import AgentProduitUniversel

def comparer_prix_multi_sites(nom_produit):
    """Comparer prix sur plusieurs sites"""
    
    agent = AgentProduitUniversel(type_produit="produit")
    
    # Scraper plusieurs sites
    sites = [
        scraper_site_a(nom_produit),
        scraper_site_b(nom_produit),
        scraper_site_c(nom_produit)
    ]
    
    # Ajouter tous les résultats
    for produits_site in sites:
        agent.ajouter_produits_depuis_dict(produits_site)
    
    # Trouver le moins cher
    top = agent.obtenir_top(n=1, critere='prix')
    
    return top[0] if top else None
```

### Exemple 3 : Surveillance de prix

```python
from agents import AgentProduitUniversel
import json
from datetime import datetime

def surveiller_prix(fichier_suivi):
    """Surveiller prix quotidiennement"""
    
    # Charger produits à suivre
    with open(fichier_suivi, 'r') as f:
        produits_suivi = json.load(f)
    
    agent = AgentProduitUniversel(type_produit="produit")
    
    # Scraper prix actuels
    for produit in produits_suivi:
        prix_actuel = scraper_prix(produit['url'])
        
        agent.ajouter_produit(
            nom=produit['nom'],
            marque=produit['marque'],
            prix=prix_actuel,
            extra={'prix_reference': produit['prix_reference']}
        )
    
    # Détecter baisses
    for p in agent.produits:
        prix_ref = p.extra.get('prix_reference', 0)
        if p.prix < prix_ref * 0.9:  # Baisse > 10%
            print(f"🔔 ALERTE : {p.nom} a baissé à {p.prix}€ !")
            envoyer_notification(p)
```

---

## 🔌 INTÉGRATION AVEC VOS OUTILS

### Avec Flask (API)

```python
from flask import Flask, request, jsonify
from agents import analyser_produits

app = Flask(__name__)

@app.route('/analyser', methods=['POST'])
def analyser():
    data = request.json
    
    resultats = analyser_produits(
        produits_data=data['produits'],
        budget_max=data['budget'],
        type_produit=data.get('type', 'produit')
    )
    
    return jsonify(resultats)

if __name__ == '__main__':
    app.run(port=5000)
```

### Avec Scrapy

```python
# Dans votre spider Scrapy
from agents import AgentProduitUniversel

class MonSpider(scrapy.Spider):
    name = 'mon_spider'
    
    def __init__(self):
        self.agent = AgentProduitUniversel(type_produit="produit")
    
    def parse(self, response):
        # Extraire produits
        for produit in response.css('.produit'):
            self.agent.ajouter_produit(
                nom=produit.css('.nom::text').get(),
                marque=produit.css('.marque::text').get(),
                prix=float(produit.css('.prix::text').get())
            )
    
    def closed(self, reason):
        # À la fin du scraping
        rapport = self.agent.generer_rapport_texte()
        print(rapport)
```

---

## 📝 STRUCTURE DES DONNÉES

### Format minimal

```python
{
    'nom': 'Nom du produit',
    'marque': 'Marque',
    'prix': 299.99
}
```

### Format complet recommandé

```python
{
    'nom': 'Nom du produit',
    'marque': 'Marque',
    'prix': 299.99,
    'note': 4.5,              # Sur 5
    'nb_avis': 500,
    'caracteristiques': ['Feature 1', 'Feature 2'],
    'url': 'https://...',
    'source': 'Site X',
    'image_url': 'https://...',
    'stock': True,
    'extra': {                 # Données personnalisées
        'couleur': 'noir',
        'poids': 200
    }
}
```

---

## 🚀 PROCHAINES ÉTAPES

1. **Testez** : Lancez `python main.py` pour voir tous les exemples
2. **Adaptez** : Modifiez les exemples selon vos besoins
3. **Intégrez** : Ajoutez l'agent dans votre code de scraping
4. **Personnalisez** : Adaptez le scoring si nécessaire

---

## 📚 RESSOURCES

- **Fichiers principaux** :
  - `agents/agent_universel.py` : Agent complet
  - `main.py` : 7 exemples d'utilisation

- **Documentation** :
  - Ce README
  - Commentaires dans le code

---

## ❓ FAQ

**Q : Ça marche avec quel type de produits ?**
R : TOUS ! Smartphones, ordinateurs, vêtements, meubles, etc.

**Q : Je dois modifier le code pour mon type de produit ?**
R : Non ! Juste changer le `type_produit` lors de la création de l'agent.

**Q : Comment adapter le scoring ?**
R : Modifiez la méthode `_calculer_score()` dans `agent_universel.py`

**Q : Je peux ajouter mes propres attributs ?**
R : Oui ! Utilisez le paramètre `extra={}` ou ajoutez des attributs à la classe Produit

**Q : Ça nécessite des dépendances ?**
R : Non ! Seulement Python 3.7+ (utilise dataclasses standard)

---

## 🎉 C'EST PARTI !

Vous avez maintenant un agent universel prêt à l'emploi pour votre scraper !

**Pour commencer :**

```bash
python main.py
```

Puis intégrez dans votre projet et adaptez selon vos besoins ! 🚀

---

**Créé avec ❤️ par Claude**

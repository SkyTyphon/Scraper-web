# 📖 GUIDE PAS À PAS - INTÉGRATION DANS VOTRE PROJET

Guide complet pour intégrer l'agent universel dans votre projet scraper existant.

---

## 🎯 OBJECTIF

Vous avez un projet scraper qui récupère des produits depuis des sites web.
Vous voulez ajouter l'agent pour analyser et recommander les meilleurs produits.

---

## 📋 ÉTAPE 1 : COPIER LES FICHIERS

### Ce que vous devez copier dans votre projet :

```bash
# Copier le dossier agents/ dans votre projet
cp -r scraper/agents/ votre_projet/

# Structure finale :
votre_projet/
├── agents/           # ← Nouveau dossier
│   ├── __init__.py
│   └── agent_universel.py
├── ... vos fichiers existants ...
```

**C'EST TOUT !** Vous avez maintenant l'agent dans votre projet.

---

## 📋 ÉTAPE 2 : IMPORTER DANS VOTRE CODE

### Dans votre fichier Python principal :

```python
# En haut de votre fichier
from agents import AgentProduitUniversel, analyser_produits
```

**Exemple complet :**

```python
# votre_scraper.py

import requests
from bs4 import BeautifulSoup
from agents import AgentProduitUniversel  # ← Ajoutez cette ligne

# ... votre code existant ...
```

---

## 📋 ÉTAPE 3 : ADAPTER VOTRE CODE DE SCRAPING

### Avant (votre code actuel) :

```python
def scraper_produits():
    """Votre fonction de scraping actuelle"""
    
    produits = []
    
    # Votre code de scraping
    for item in soup.select('.produit'):
        produit = {
            'nom': item.select_one('.nom').text,
            'marque': item.select_one('.marque').text,
            'prix': float(item.select_one('.prix').text.replace('€', ''))
        }
        produits.append(produit)
    
    return produits
```

### Après (avec l'agent) :

```python
from agents import AgentProduitUniversel

def scraper_et_analyser():
    """Nouvelle version avec analyse"""
    
    # 1. Votre scraping existant (INCHANGÉ)
    produits = []
    for item in soup.select('.produit'):
        produit = {
            'nom': item.select_one('.nom').text,
            'marque': item.select_one('.marque').text,
            'prix': float(item.select_one('.prix').text.replace('€', ''))
        }
        produits.append(produit)
    
    # 2. NOUVEAU : Analyser avec l'agent
    agent = AgentProduitUniversel(type_produit="votre_type")
    agent.ajouter_produits_depuis_dict(produits)
    
    # 3. NOUVEAU : Obtenir recommandations
    top_3 = agent.obtenir_top(n=3, budget_max=500)
    
    # 4. Retourner les résultats
    return {
        'tous_produits': produits,
        'top_3': [p.to_dict() for p in top_3],
        'meilleur': top_3[0].to_dict() if top_3 else None
    }
```

**Vous avez juste ajouté 4 lignes !**

---

## 📋 ÉTAPE 4 : EXEMPLES CONCRETS SELON VOS BESOINS

### CAS 1 : Vous avez déjà une fonction qui retourne des produits

**Votre code actuel :**
```python
def get_produits():
    # ... scraping ...
    return liste_produits
```

**Modification minimale :**
```python
from agents import analyser_produits  # Import ultra-simple

def get_produits_avec_analyse():
    # Votre code existant
    produits = get_produits()
    
    # Ajouter analyse (1 ligne !)
    resultats = analyser_produits(produits, budget_max=500, type_produit="smartphone")
    
    return resultats
```

### CAS 2 : Vous utilisez Scrapy

**Dans votre spider :**
```python
# spider.py

from agents import AgentProduitUniversel
import scrapy

class MonSpider(scrapy.Spider):
    name = 'mon_spider'
    
    def __init__(self):
        super().__init__()
        # Ajouter agent
        self.agent = AgentProduitUniversel(type_produit="produit")
    
    def parse(self, response):
        # Votre code de parsing existant
        for produit in response.css('.produit'):
            nom = produit.css('.nom::text').get()
            marque = produit.css('.marque::text').get()
            prix = float(produit.css('.prix::text').get())
            
            # Ajouter à l'agent
            self.agent.ajouter_produit(
                nom=nom,
                marque=marque,
                prix=prix
            )
            
            # Votre code yield existant
            yield {'nom': nom, 'marque': marque, 'prix': prix}
    
    def closed(self, reason):
        # À la fin du scraping, analyser
        rapport = self.agent.generer_rapport_texte(budget_max=500)
        print(rapport)
        
        # Exporter résultats
        self.agent.exporter_json('resultats.json')
```

### CAS 3 : Vous sauvegardez dans une base de données

**Votre code actuel :**
```python
def sauvegarder_produits(produits):
    for p in produits:
        db.save(p)
```

**Avec agent :**
```python
from agents import AgentProduitUniversel

def sauvegarder_et_analyser(produits):
    # 1. Analyser AVANT de sauvegarder
    agent = AgentProduitUniversel(type_produit="produit")
    agent.ajouter_produits_depuis_dict(produits)
    
    # 2. Ajouter score qualité/prix à chaque produit
    for i, p in enumerate(produits):
        p['score_qualite_prix'] = agent.produits[i].score_qualite_prix
    
    # 3. Sauvegarder (votre code existant)
    for p in produits:
        db.save(p)
    
    # 4. Retourner les meilleurs
    top = agent.obtenir_top(n=5)
    return top
```

### CAS 4 : Vous avez une API

**Avant :**
```python
@app.route('/produits', methods=['GET'])
def get_produits():
    produits = scraper_site()
    return jsonify(produits)
```

**Après :**
```python
from agents import analyser_produits

@app.route('/produits', methods=['GET'])
def get_produits():
    budget = request.args.get('budget', 500)
    
    # Scraper
    produits = scraper_site()
    
    # Analyser
    resultats = analyser_produits(produits, budget_max=float(budget))
    
    return jsonify({
        'tous_produits': produits,
        'recommandations': resultats
    })
```

---

## 📋 ÉTAPE 5 : PERSONNALISER LE SCORING (OPTIONNEL)

Si vous voulez adapter le scoring à votre domaine :

**Fichier : `agents/agent_universel.py`**

Cherchez la méthode `_calculer_score` (ligne ~90) :

```python
def _calculer_score(self) -> float:
    score = 0
    
    # MODIFIEZ ICI selon vos besoins !
    
    # 40% basé sur note (gardez ou modifiez)
    if self.note > 0:
        score += (self.note / 5) * 40
    
    # 30% basé sur prix (adaptez le seuil)
    prix_reference = 500  # ← CHANGEZ SELON VOTRE DOMAINE
    if self.prix > 0:
        ratio_prix = max(0, 1 - (self.prix / prix_reference))
        score += ratio_prix * 30
    
    # 20% basé sur popularité
    if self.nb_avis >= 200:
        score += 20
    # ... etc
    
    return min(score, 100)
```

**Exemples de personnalisation :**

```python
# Pour vêtements (prix bas = mieux)
prix_reference = 100

# Pour électronique haut de gamme (prix élevé acceptable)
prix_reference = 2000

# Pour privilégier la note
score += (self.note / 5) * 60  # 60% au lieu de 40%

# Pour ajouter critère personnalisé
if 'bio' in self.caracteristiques:
    score += 10  # Bonus produits bio
```

---

## 📋 ÉTAPE 6 : TESTER

### Test simple :

```python
# test_agent.py

from agents import AgentProduitUniversel

# Créer agent
agent = AgentProduitUniversel(type_produit="test")

# Ajouter produit test
agent.ajouter_produit(
    nom="Produit Test",
    marque="Test",
    prix=99.99,
    note=4.5,
    nb_avis=100
)

# Vérifier
print(f"Agent a {len(agent)} produits")
print(f"Score : {agent.produits[0].score_qualite_prix:.1f}/100")

# Si ça affiche un score, ça marche ! ✅
```

Lancez :
```bash
python test_agent.py
```

Si vous voyez un score, **c'est bon !** ✅

---

## 📋 ÉTAPE 7 : UTILISER DANS VOTRE WORKFLOW

### Workflow typique :

```python
# 1. Scraper
produits = scraper_sites(['site1.com', 'site2.com'])

# 2. Nettoyer (votre code)
produits_clean = nettoyer_produits(produits)

# 3. NOUVEAU : Analyser
from agents import analyser_produits
resultats = analyser_produits(produits_clean, budget_max=500)

# 4. Sauvegarder top produits
sauvegarder_bdd(resultats['top_recommandations'])

# 5. Envoyer notifications
if resultats['meilleur_produit']:
    envoyer_email(resultats['meilleur_produit'])
```

---

## 🎯 CHECKLIST COMPLÈTE

- [ ] Dossier `agents/` copié dans votre projet
- [ ] Import ajouté : `from agents import AgentProduitUniversel`
- [ ] Agent créé : `agent = AgentProduitUniversel(type_produit="...")`
- [ ] Produits ajoutés : `agent.ajouter_produits_depuis_dict(produits)`
- [ ] Résultats obtenus : `top = agent.obtenir_top(n=3)`
- [ ] Test effectué : `python test_agent.py`
- [ ] Intégré dans workflow principal

---

## 🆘 PROBLÈMES COURANTS

### Erreur : ModuleNotFoundError: No module named 'agents'

**Solution :** Vérifiez que le dossier `agents/` est bien dans votre projet :
```bash
ls votre_projet/agents/
# Doit afficher : __init__.py  agent_universel.py
```

### Erreur : No module named 'dataclasses'

**Solution :** Python < 3.7. Mettez à jour :
```bash
python --version  # Doit être >= 3.7
```

### Les scores sont tous pareils

**Solution :** Vérifiez que vous passez bien `note`, `nb_avis`, etc. :
```python
# Mauvais (juste prix)
agent.ajouter_produit(nom="X", marque="Y", prix=99)

# Bon (avec note et avis)
agent.ajouter_produit(
    nom="X", 
    marque="Y", 
    prix=99,
    note=4.5,      # ← Important !
    nb_avis=500    # ← Important !
)
```

---

## 🎉 FÉLICITATIONS !

Vous avez maintenant intégré l'agent dans votre projet !

**Prochaines étapes :**
1. Testez avec vos vraies données
2. Adaptez le scoring si besoin
3. Ajoutez des filtres personnalisés
4. Automatisez l'analyse

**Besoin d'aide ?** Consultez :
- `README.md` : Documentation complète
- `main.py` : 7 exemples d'utilisation
- Code commenté dans `agent_universel.py`

🚀 **Bon scraping !**

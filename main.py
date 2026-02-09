"""
SCRAPER - FICHIER PRINCIPAL
============================

Exemples d'utilisation de l'agent universel dans votre projet scraper.

Auteur : Claude
Date : 2026-02-08
"""

from agents import AgentProduitUniversel, Produit, analyser_produits
import json


# ============================================================================
# EXEMPLE 1 : UTILISATION LA PLUS SIMPLE
# ============================================================================

def exemple_simple():
    """Exemple minimal - Ajouter et analyser des produits"""
    
    print("=" * 80)
    print("EXEMPLE 1 : Utilisation simple")
    print("=" * 80)
    
    # Créer l'agent (adaptez le type de produit)
    agent = AgentProduitUniversel(type_produit="smartphone")
    
    # Ajouter des produits manuellement
    agent.ajouter_produit(
        nom="iPhone 15 Pro",
        marque="Apple",
        prix=1199,
        note=4.7,
        nb_avis=2500,
        caracteristiques=["5G", "256GB", "Titanium"],
        stock=True
    )
    
    agent.ajouter_produit(
        nom="Galaxy S24 Ultra",
        marque="Samsung",
        prix=1399,
        note=4.6,
        nb_avis=1800,
        caracteristiques=["5G", "512GB", "S Pen"]
    )
    
    agent.ajouter_produit(
        nom="Pixel 8 Pro",
        marque="Google",
        prix=999,
        note=4.5,
        nb_avis=900,
        caracteristiques=["5G", "128GB", "AI Camera"]
    )
    
    # Générer rapport
    rapport = agent.generer_rapport_texte(budget_max=1200)
    print(rapport)
    
    # Obtenir le meilleur
    top = agent.obtenir_top(n=1, budget_max=1200)
    if top:
        meilleur = top[0]
        print(f"🏆 Meilleur choix : {meilleur.marque} {meilleur.nom}")
        print(f"   Prix : {meilleur.prix}€")
        print(f"   Score : {meilleur.score_qualite_prix:.1f}/100")


# ============================================================================
# EXEMPLE 2 : DEPUIS DICTIONNAIRES (Typique après scraping)
# ============================================================================

def exemple_depuis_dict():
    """Exemple avec données depuis scraping/API"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 2 : Depuis dictionnaires (après scraping)")
    print("=" * 80)
    
    # Simuler des données que vous auriez scrapées
    produits_scrapes = [
        {
            'nom': 'MacBook Air M2',
            'marque': 'Apple',
            'prix': 1299,
            'note': 4.8,
            'nb_avis': 3200,
            'caracteristiques': ['M2', '8GB RAM', '256GB SSD'],
            'url': 'https://www.apple.com/...',
            'source': 'Apple Store'
        },
        {
            'nom': 'ThinkPad X1 Carbon',
            'marque': 'Lenovo',
            'prix': 1599,
            'note': 4.6,
            'nb_avis': 1500,
            'caracteristiques': ['i7', '16GB RAM', '512GB SSD'],
            'url': 'https://www.lenovo.com/...',
            'source': 'Lenovo'
        },
        {
            'nom': 'XPS 13',
            'marque': 'Dell',
            'prix': 1199,
            'note': 4.5,
            'nb_avis': 1100,
            'caracteristiques': ['i5', '8GB RAM', '256GB SSD'],
            'url': 'https://www.dell.com/...',
            'source': 'Dell'
        }
    ]
    
    # Créer agent et charger données
    agent = AgentProduitUniversel(type_produit="ordinateur portable")
    nb_ajoutes = agent.ajouter_produits_depuis_dict(produits_scrapes)
    
    print(f"\n✅ {nb_ajoutes} produits ajoutés")
    
    # Obtenir recommandations
    recommandations = agent.obtenir_recommandations(
        budget_max=1400,
        note_min=4.5,
        top_n=2
    )
    
    print(f"\n🎯 Recommandations pour budget 1400€ :")
    for i, produit in enumerate(recommandations['top_recommandations'], 1):
        print(f"\n{i}. {produit['marque']} {produit['nom']}")
        print(f"   Prix : {produit['prix']}€")
        print(f"   Score : {produit['score_qualite_prix']:.1f}/100")
        print(f"   Note : {produit['note']}/5 ⭐ ({produit['nb_avis']} avis)")


# ============================================================================
# EXEMPLE 3 : FONCTION RÉUTILISABLE (Recommandé pour intégration)
# ============================================================================

def rechercher_et_recommander(produits_data, budget, type_produit="produit"):
    """
    FONCTION RÉUTILISABLE - C'EST CELLE-CI QUE VOUS UTILISEREZ !
    
    Intégrez cette fonction dans votre projet pour analyser
    n'importe quelle liste de produits.
    
    Args:
        produits_data: Liste de dicts avec vos produits
        budget: Budget maximum
        type_produit: Type de produit
    
    Returns:
        Dict avec toutes les analyses et recommandations
    """
    agent = AgentProduitUniversel(type_produit)
    agent.ajouter_produits_depuis_dict(produits_data)
    
    # Obtenir stats
    stats = agent.obtenir_statistiques()
    
    # Obtenir top 3
    top_3 = agent.obtenir_top(n=3, budget_max=budget)
    
    # Obtenir recommandations complètes
    recommandations = agent.obtenir_recommandations(budget_max=budget, top_n=5)
    
    return {
        'statistiques': stats,
        'top_3': [p.to_dict() for p in top_3],
        'recommandations_completes': recommandations,
        'meilleur_produit': top_3[0].to_dict() if top_3 else None,
        'rapport_texte': agent.generer_rapport_texte(budget_max=budget)
    }


def exemple_fonction_reutilisable():
    """Exemple d'utilisation de la fonction réutilisable"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 3 : Fonction réutilisable")
    print("=" * 80)
    
    # Vos produits (d'où qu'ils viennent)
    mes_produits = [
        {'nom': 'AirPods Pro 2', 'marque': 'Apple', 'prix': 279, 'note': 4.7, 'nb_avis': 5000},
        {'nom': 'WH-1000XM5', 'marque': 'Sony', 'prix': 399, 'note': 4.8, 'nb_avis': 3200},
        {'nom': 'QuietComfort Ultra', 'marque': 'Bose', 'prix': 429, 'note': 4.6, 'nb_avis': 1800},
        {'nom': 'Galaxy Buds2 Pro', 'marque': 'Samsung', 'prix': 229, 'note': 4.5, 'nb_avis': 2100}
    ]
    
    # Analyser
    resultats = rechercher_et_recommander(
        produits_data=mes_produits,
        budget=350,
        type_produit="écouteurs"
    )
    
    # Afficher résultats
    print(f"\n📊 Statistiques :")
    print(f"   Produits analysés : {resultats['statistiques']['nb_produits']}")
    print(f"   Prix moyen : {resultats['statistiques']['prix_moyen']:.2f}€")
    print(f"   Note moyenne : {resultats['statistiques']['note_moyenne']:.1f}/5")
    
    print(f"\n🏆 Meilleur produit :")
    if resultats['meilleur_produit']:
        p = resultats['meilleur_produit']
        print(f"   {p['marque']} {p['nom']}")
        print(f"   Prix : {p['prix']}€ | Score : {p['score_qualite_prix']:.1f}/100")


# ============================================================================
# EXEMPLE 4 : DEPUIS FICHIER JSON
# ============================================================================

def exemple_depuis_json():
    """Exemple de chargement depuis fichier JSON"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 4 : Depuis fichier JSON")
    print("=" * 80)
    
    # Créer fichier JSON exemple
    data_exemple = [
        {'nom': 'TV OLED 55"', 'marque': 'LG', 'prix': 1299, 'note': 4.7, 'nb_avis': 890},
        {'nom': 'TV QLED 55"', 'marque': 'Samsung', 'prix': 1199, 'note': 4.6, 'nb_avis': 1200},
        {'nom': 'Bravia XR 55"', 'marque': 'Sony', 'prix': 1499, 'note': 4.8, 'nb_avis': 650}
    ]
    
    fichier = 'data/produits_exemple.json'
    with open(fichier, 'w', encoding='utf-8') as f:
        json.dump(data_exemple, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fichier créé : {fichier}")
    
    # Charger depuis JSON
    agent = AgentProduitUniversel(type_produit="TV")
    nb_charges = agent.ajouter_produits_depuis_json(fichier)
    
    print(f"✅ {nb_charges} produits chargés depuis JSON")
    
    # Analyser
    rapport = agent.generer_rapport_texte(budget_max=1300)
    print(rapport)


# ============================================================================
# EXEMPLE 5 : FILTRES AVANCÉS
# ============================================================================

def exemple_filtres():
    """Exemple d'utilisation des filtres"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 5 : Filtres avancés")
    print("=" * 80)
    
    # Créer agent avec plusieurs produits
    agent = AgentProduitUniversel(type_produit="smartphone")
    
    produits = [
        {'nom': 'iPhone 15', 'marque': 'Apple', 'prix': 999, 'note': 4.7, 'nb_avis': 3000, 
         'caracteristiques': ['5G', 'iOS', '128GB']},
        {'nom': 'iPhone 15 Pro', 'marque': 'Apple', 'prix': 1299, 'note': 4.8, 'nb_avis': 2000,
         'caracteristiques': ['5G', 'iOS', '256GB', 'Titanium']},
        {'nom': 'Galaxy S24', 'marque': 'Samsung', 'prix': 899, 'note': 4.6, 'nb_avis': 1500,
         'caracteristiques': ['5G', 'Android', '256GB']},
        {'nom': 'Pixel 8', 'marque': 'Google', 'prix': 699, 'note': 4.5, 'nb_avis': 800,
         'caracteristiques': ['5G', 'Android', '128GB']},
    ]
    
    agent.ajouter_produits_depuis_dict(produits)
    
    print(f"✅ {len(agent)} produits ajoutés")
    
    # Filtrer par budget
    print(f"\n💰 Produits à moins de 1000€ :")
    for p in agent.filtrer_par_budget(1000):
        print(f"   - {p.marque} {p.nom} : {p.prix}€")
    
    # Filtrer par marque
    print(f"\n🏢 Produits Apple uniquement :")
    for p in agent.filtrer_par_marque(['Apple']):
        print(f"   - {p.nom} : {p.prix}€")
    
    # Filtrer par note
    print(f"\n⭐ Produits avec note >= 4.7 :")
    for p in agent.filtrer_par_note(4.7):
        print(f"   - {p.marque} {p.nom} : {p.note}/5")
    
    # Filtrer par caractéristique
    print(f"\n📱 Produits avec '5G' :")
    for p in agent.filtrer_par_caracteristique('5G'):
        print(f"   - {p.marque} {p.nom}")
    
    # Filtre personnalisé
    print(f"\n🎯 Produits Samsung avec note > 4.5 :")
    samsung_top = agent.filtrer_personnalise(
        lambda p: p.marque == 'Samsung' and p.note > 4.5
    )
    for p in samsung_top:
        print(f"   - {p.nom} : {p.note}/5 ⭐")


# ============================================================================
# EXEMPLE 6 : EXPORT ET SAUVEGARDE
# ============================================================================

def exemple_export():
    """Exemple d'export des résultats"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 6 : Export et sauvegarde")
    print("=" * 80)
    
    # Créer agent avec données
    agent = AgentProduitUniversel(type_produit="tablette")
    
    produits = [
        {'nom': 'iPad Air', 'marque': 'Apple', 'prix': 699, 'note': 4.7, 'nb_avis': 2500},
        {'nom': 'iPad Pro 11"', 'marque': 'Apple', 'prix': 999, 'note': 4.8, 'nb_avis': 1800},
        {'nom': 'Galaxy Tab S9', 'marque': 'Samsung', 'prix': 799, 'note': 4.6, 'nb_avis': 1200},
        {'nom': 'Surface Pro 9', 'marque': 'Microsoft', 'prix': 1099, 'note': 4.5, 'nb_avis': 900}
    ]
    
    agent.ajouter_produits_depuis_dict(produits)
    
    # Exporter en JSON
    fichier_export = 'data/resultats_tablettes.json'
    agent.exporter_json(fichier_export, budget_max=900)
    
    print(f"\n✅ Résultats exportés dans : {fichier_export}")
    print(f"   Vous pouvez maintenant utiliser ce fichier dans d'autres scripts !")


# ============================================================================
# EXEMPLE 7 : UTILISATION AVEC FONCTION ULTRA-SIMPLE
# ============================================================================

def exemple_ultra_simple():
    """Utilisation avec la fonction helper analyser_produits()"""
    
    print("\n" + "=" * 80)
    print("EXEMPLE 7 : Fonction ultra-simple analyser_produits()")
    print("=" * 80)
    
    # Vos produits
    mes_produits = [
        {'nom': 'Produit A', 'marque': 'Samsung', 'prix': 299, 'note': 4.5, 'nb_avis': 500},
        {'nom': 'Produit B', 'marque': 'LG', 'prix': 399, 'note': 4.7, 'nb_avis': 350},
        {'nom': 'Produit C', 'marque': 'Sony', 'prix': 499, 'note': 4.8, 'nb_avis': 200}
    ]
    
    # Analyser EN UNE LIGNE !
    resultats = analyser_produits(
        produits_data=mes_produits,
        budget_max=400,
        type_produit="produit"
    )
    
    # Afficher meilleur produit
    if resultats['meilleur_produit']:
        p = resultats['meilleur_produit']
        print(f"\n🏆 Meilleur produit trouvé :")
        print(f"   {p['marque']} {p['nom']}")
        print(f"   Prix : {p['prix']}€")
        print(f"   Score : {p['score_qualite_prix']:.1f}/100")
        print(f"   Note : {p['note']}/5 ⭐")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Lancer tous les exemples"""
    
    print("\n" + "🚀" * 40)
    print("AGENT UNIVERSEL - EXEMPLES D'UTILISATION")
    print("🚀" * 40 + "\n")
    
    # Lancer tous les exemples
    exemple_simple()
    exemple_depuis_dict()
    exemple_fonction_reutilisable()
    exemple_depuis_json()
    exemple_filtres()
    exemple_export()
    exemple_ultra_simple()
    
    print("\n" + "✅" * 40)
    print("TOUS LES EXEMPLES TERMINÉS !")
    print("✅" * 40)
    print("\nMaintenant, intégrez ces exemples dans VOTRE projet scraper ! 🚀")
    print("Voir README.md pour guide complet d'intégration.\n")


if __name__ == "__main__":
    main()

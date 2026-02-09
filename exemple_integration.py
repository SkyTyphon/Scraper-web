#!/usr/bin/env python3
"""
EXEMPLE SIMPLE - SCRAPER + AGENT
=================================

Ce fichier montre comment intégrer l'agent dans un scraper simple.

Utilisez-le comme point de départ pour votre projet !
"""

from agents import AgentProduitUniversel, analyser_produits


# ============================================================================
# EXEMPLE 1 : SCRAPER FICTIF + ANALYSE
# ============================================================================

def exemple_scraper_simple():
    """
    Simule un scraper basique puis analyse les produits
    
    Remplacez cette fonction par votre vrai code de scraping !
    """
    
    print("\n" + "="*60)
    print("EXEMPLE 1 : Scraper simple + Analyse")
    print("="*60)
    
    # ========================================
    # 1. SCRAPING (simulé ici)
    # ========================================
    print("\n[1/3] Scraping des produits...")
    
    # Dans votre vrai projet, vous feriez :
    # import requests
    # from bs4 import BeautifulSoup
    # response = requests.get('https://votre-site.com')
    # soup = BeautifulSoup(response.text, 'html.parser')
    # etc.
    
    # Pour cet exemple, on simule des données scrapées :
    produits_scrapes = [
        {
            'nom': 'Smartphone Galaxy S24',
            'marque': 'Samsung',
            'prix': 899,
            'note': 4.6,
            'nb_avis': 1500,
            'url': 'https://exemple.com/galaxy-s24'
        },
        {
            'nom': 'iPhone 15',
            'marque': 'Apple',
            'prix': 999,
            'note': 4.7,
            'nb_avis': 3000,
            'url': 'https://exemple.com/iphone-15'
        },
        {
            'nom': 'Pixel 8',
            'marque': 'Google',
            'prix': 699,
            'note': 4.5,
            'nb_avis': 800,
            'url': 'https://exemple.com/pixel-8'
        }
    ]
    
    print(f"✅ {len(produits_scrapes)} produits scrapés")
    
    # ========================================
    # 2. ANALYSE AVEC L'AGENT
    # ========================================
    print("\n[2/3] Analyse des produits...")
    
    # Créer l'agent
    agent = AgentProduitUniversel(type_produit="smartphone")
    
    # Charger les produits
    agent.ajouter_produits_depuis_dict(produits_scrapes)
    
    # Obtenir recommandations
    top_3 = agent.obtenir_top(n=3, budget_max=1000)
    
    print(f"✅ Analyse terminée")
    
    # ========================================
    # 3. AFFICHAGE DES RÉSULTATS
    # ========================================
    print("\n[3/3] Résultats :")
    print("\n🏆 TOP 3 des meilleurs smartphones (budget 1000€) :\n")
    
    for i, produit in enumerate(top_3, 1):
        print(f"{i}. {produit.marque} {produit.nom}")
        print(f"   💰 Prix : {produit.prix}€")
        print(f"   ⭐ Note : {produit.note}/5 ({produit.nb_avis} avis)")
        print(f"   📊 Score qualité/prix : {produit.score_qualite_prix:.1f}/100")
        print()
    
    # Export en JSON
    agent.exporter_json('data/resultats_smartphones.json', budget_max=1000)
    print("✅ Résultats exportés dans data/resultats_smartphones.json")


# ============================================================================
# EXEMPLE 2 : FONCTION RÉUTILISABLE
# ============================================================================

def scraper_et_analyser(type_produit, budget_max=500):
    """
    Fonction réutilisable pour scraper et analyser
    
    Args:
        type_produit: Type de produit à scraper
        budget_max: Budget maximum
    
    Returns:
        Dict avec les résultats de l'analyse
    """
    
    print(f"\n🔍 Scraping de {type_produit}...")
    
    # 1. SCRAPING
    # Ici, remplacez par votre vrai code de scraping
    produits = []
    
    # Exemple : scraper plusieurs sites
    # for site in ['site1.com', 'site2.com', 'site3.com']:
    #     produits.extend(scraper_site(site, type_produit))
    
    # Pour l'exemple, on simule :
    produits = [
        {'nom': f'{type_produit} A', 'marque': 'Marque A', 'prix': 299, 'note': 4.5},
        {'nom': f'{type_produit} B', 'marque': 'Marque B', 'prix': 399, 'note': 4.7},
        {'nom': f'{type_produit} C', 'marque': 'Marque C', 'prix': 499, 'note': 4.8}
    ]
    
    # 2. ANALYSE
    resultats = analyser_produits(
        produits_data=produits,
        budget_max=budget_max,
        type_produit=type_produit
    )
    
    return resultats


# ============================================================================
# EXEMPLE 3 : INTÉGRATION AVEC VOTRE SCRAPER EXISTANT
# ============================================================================

def votre_fonction_scraping_existante():
    """
    Exemple de votre fonction de scraping existante
    
    Remplacez ceci par votre vrai code !
    """
    # Votre code de scraping actuel
    produits = [
        # Vos produits scrapés
    ]
    return produits


def votre_fonction_avec_agent():
    """
    Version améliorée avec l'agent
    
    Copiez-collez votre fonction de scraping ici et ajoutez l'agent !
    """
    
    # 1. Votre scraping existant (INCHANGÉ)
    produits = votre_fonction_scraping_existante()
    
    # 2. AJOUT : Analyse avec l'agent (3 lignes !)
    agent = AgentProduitUniversel(type_produit="votre_type")
    agent.ajouter_produits_depuis_dict(produits)
    top = agent.obtenir_top(n=5, budget_max=500)
    
    # 3. Retourner les résultats enrichis
    return {
        'tous_produits': produits,
        'top_5': [p.to_dict() for p in top],
        'meilleur': top[0].to_dict() if top else None
    }


# ============================================================================
# EXEMPLE 4 : SURVEILLANCE DE PRIX QUOTIDIENNE
# ============================================================================

def surveiller_prix_quotidien():
    """
    Exemple de surveillance quotidienne des prix
    
    Lancez cette fonction chaque jour (cron, scheduler, etc.)
    """
    import json
    from datetime import datetime
    
    print("\n" + "="*60)
    print("SURVEILLANCE DE PRIX QUOTIDIENNE")
    print("="*60)
    
    # 1. Charger les produits à surveiller
    # (créez ce fichier avec les produits que vous suivez)
    try:
        with open('data/produits_surveilles.json', 'r') as f:
            produits_suivi = json.load(f)
    except FileNotFoundError:
        print("❌ Créez d'abord data/produits_surveilles.json")
        return
    
    # 2. Scraper les prix actuels
    agent = AgentProduitUniversel(type_produit="produit")
    
    for produit in produits_suivi:
        # Scraper le prix actuel (à adapter selon votre code)
        # prix_actuel = scraper_prix(produit['url'])
        prix_actuel = produit['prix']  # Exemple
        
        agent.ajouter_produit(
            nom=produit['nom'],
            marque=produit['marque'],
            prix=prix_actuel,
            extra={'prix_reference': produit.get('prix_reference', prix_actuel)}
        )
    
    # 3. Détecter les baisses de prix
    alertes = []
    for p in agent.produits:
        prix_ref = p.extra.get('prix_reference', 0)
        if prix_ref > 0 and p.prix < prix_ref * 0.9:  # Baisse > 10%
            alertes.append(p)
            print(f"🔔 ALERTE : {p.nom} a baissé à {p.prix}€ (-{((prix_ref-p.prix)/prix_ref*100):.0f}%)")
    
    # 4. Envoyer notifications si nécessaire
    if alertes:
        print(f"\n✉️  {len(alertes)} alerte(s) de prix détectée(s)")
        # Envoyez un email, une notif Telegram, etc.
    else:
        print("\n✅ Aucune baisse de prix significative")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "🚀"*30)
    print("EXEMPLES D'INTÉGRATION SCRAPER + AGENT")
    print("🚀"*30)
    
    # Lancer les exemples
    exemple_scraper_simple()
    
    print("\n" + "="*60)
    print("EXEMPLE 2 : Fonction réutilisable")
    print("="*60)
    
    resultats = scraper_et_analyser("ordinateur portable", budget_max=1500)
    if resultats['meilleur_produit']:
        p = resultats['meilleur_produit']
        print(f"\n🏆 Meilleur choix : {p['marque']} {p['nom']} - {p['prix']}€")
    
    print("\n" + "="*60)
    print("\n✅ EXEMPLES TERMINÉS !")
    print("\nMaintenant, adaptez ces exemples à VOTRE projet !")
    print("Consultez docs/GUIDE_INTEGRATION_PAS_A_PAS.md pour plus d'aide.\n")

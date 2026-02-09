"""
SCRAPER - FICHIER PRINCIPAL
============================

Lance une recherche interactive de produits.
Les parametres sont demandes a l'utilisateur au demarrage.

Auteur : Claude
Date : 2026-02-08
"""

from agents import AgentProduitUniversel, Produit, analyser_produits
import json
import os


# ============================================================================
# SAISIE INTERACTIVE DES PARAMETRES
# ============================================================================

def demander_parametres():
    """
    Demande tous les parametres de recherche a l'utilisateur.

    Returns:
        dict avec les cles :
            - produit (str)
            - prix_min (float ou None)
            - prix_max (float ou None)
            - livrable (bool)
            - lieu (str ou None)
            - distance_km (int ou None)
    """

    print("\n" + "=" * 60)
    print("  CONFIGURATION DE LA RECHERCHE")
    print("=" * 60)

    # --- Produit ---
    produit = ""
    while not produit.strip():
        produit = input("\nProduit recherche : ").strip()
        if not produit:
            print("  Veuillez saisir un nom de produit.")

    # --- Prix min ---
    prix_min = None
    saisie = input("Prix minimum (EUR) [laisser vide = pas de minimum] : ").strip()
    if saisie:
        try:
            prix_min = float(saisie)
        except ValueError:
            print("  Valeur ignoree (non numerique).")

    # --- Prix max ---
    prix_max = None
    saisie = input("Prix maximum (EUR) [laisser vide = pas de maximum] : ").strip()
    if saisie:
        try:
            prix_max = float(saisie)
        except ValueError:
            print("  Valeur ignoree (non numerique).")

    # --- Livraison ---
    saisie_livrable = input("Le produit est-il livrable ? (o/n) [o] : ").strip().lower()
    livrable = saisie_livrable != "n"

    lieu = None
    distance_km = None

    if not livrable:
        # --- Lieu ---
        lieu = input("Lieu de recherche (ville ou code postal) : ").strip() or None

        # --- Distance ---
        if lieu:
            saisie = input("Distance maximale en km [30] : ").strip()
            if saisie:
                try:
                    distance_km = int(saisie)
                except ValueError:
                    print("  Valeur ignoree, 30 km par defaut.")
                    distance_km = 30
            else:
                distance_km = 30

    # --- Resume ---
    print("\n" + "-" * 60)
    print("  RESUME DE LA RECHERCHE")
    print("-" * 60)
    print(f"  Produit      : {produit}")
    if prix_min is not None:
        print(f"  Prix min     : {prix_min} EUR")
    if prix_max is not None:
        print(f"  Prix max     : {prix_max} EUR")
    print(f"  Livrable     : {'Oui' if livrable else 'Non'}")
    if not livrable and lieu:
        print(f"  Lieu         : {lieu}")
        print(f"  Distance max : {distance_km} km")
    print("-" * 60)

    # Confirmation
    confirmer = input("\nLancer la recherche ? (o/n) [o] : ").strip().lower()
    if confirmer == "n":
        print("Recherche annulee.")
        return None

    return {
        "produit": produit,
        "prix_min": prix_min,
        "prix_max": prix_max,
        "livrable": livrable,
        "lieu": lieu,
        "distance_km": distance_km,
    }


# ============================================================================
# RECHERCHE ET ANALYSE
# ============================================================================

def lancer_recherche(params):
    """
    Lance la recherche et l'analyse avec les parametres donnes.

    Args:
        params: dict retourne par demander_parametres()
    """

    print(f"\nRecherche de '{params['produit']}' en cours...\n")

    # Charger les produits depuis le fichier JSON d'exemple
    fichier_data = os.path.join("data", "produits_exemple.json")
    agent = AgentProduitUniversel(type_produit=params["produit"])

    if os.path.exists(fichier_data):
        nb = agent.ajouter_produits_depuis_json(fichier_data)
        print(f"{nb} produit(s) charge(s) depuis {fichier_data}")
    else:
        print(f"Aucun fichier de donnees trouve ({fichier_data}).")
        print("Ajoutez vos produits dans data/produits_exemple.json")
        return

    # Appliquer les filtres
    produits_filtres = list(agent.produits)

    if params["prix_min"] is not None:
        produits_filtres = [
            p for p in produits_filtres if p.prix >= params["prix_min"]
        ]

    if params["prix_max"] is not None:
        produits_filtres = [
            p for p in produits_filtres if p.prix <= params["prix_max"]
        ]

    if not produits_filtres:
        print("\nAucun produit ne correspond a vos criteres.")
        return

    # Creer un nouvel agent avec les produits filtres
    agent_filtre = AgentProduitUniversel(type_produit=params["produit"])
    for p in produits_filtres:
        agent_filtre.ajouter_produit(
            nom=p.nom,
            marque=p.marque,
            prix=p.prix,
            note=p.note,
            nb_avis=p.nb_avis,
            caracteristiques=p.caracteristiques,
            url=p.url,
            source=p.source,
            stock=p.stock,
        )

    # Generer rapport
    rapport = agent_filtre.generer_rapport_texte(budget_max=params["prix_max"])
    print(rapport)

    # Exporter les resultats
    os.makedirs("data", exist_ok=True)
    fichier_export = os.path.join("data", f"resultats_{params['produit'].replace(' ', '_').lower()}.json")
    agent_filtre.exporter_json(fichier_export, budget_max=params["prix_max"])

    # Afficher les infos de localisation si pertinentes
    if not params["livrable"] and params["lieu"]:
        print(f"\nRecherche locale : {params['lieu']} (rayon {params['distance_km']} km)")
        print("(Le filtrage geographique sera actif une fois connecte a une source de donnees reelle.)")

    print(f"\nResultats exportes dans : {fichier_export}")


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Point d'entree : demander les parametres puis lancer la recherche."""

    print("\n" + "=" * 60)
    print("  AGENT UNIVERSEL - RECHERCHE DE PRODUITS")
    print("=" * 60)

    params = demander_parametres()
    if params is None:
        return

    lancer_recherche(params)

    print("\nRecherche terminee.")


if __name__ == "__main__":
    main()

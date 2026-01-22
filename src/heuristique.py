import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
from instance import chargerInstance, obtenirMatriceDistances
from visualisation import construireRingStar

def plusProcheVoisin(matrice_dist, depart=0):
    """
    Heuristique du plus proche voisin pour le TSP.
    Commence à une ville et choisit toujours la ville non visitée la plus proche.
    
    Args:
        matrice_dist: Matrice de distances (numpy array)
        depart: Indice de la ville de départ (par défaut 0)
        
    Returns:
        Tuple (chemin_indices, coût_total)
    """
    n = len(matrice_dist)
    visite = [False] * n
    chemin_indices = [depart]
    visite[depart] = True
    cout_total = 0
    
    actuel = depart
    for _ in range(n - 1):
        # Trouver le plus proche voisin non visité
        distances = matrice_dist[actuel].copy()
        # Mettre les villes visitées à l'infini pour les ignorer
        for i in range(n):
            if visite[i]:
                distances[i] = np.inf
        
        prochain = np.argmin(distances)
        chemin_indices.append(prochain)
        visite[prochain] = True
        cout_total += matrice_dist[actuel][prochain]
        actuel = prochain
    
    # Retour au point de départ
    cout_total += matrice_dist[chemin_indices[-1]][chemin_indices[0]]
    
    return chemin_indices, cout_total

def resoudreRingStar_Heuristique(fichier_tsp, nb_stations_ring):
    """
    Résout le problème Ring-Star avec une heuristique.
    
    Args:
        fichier_tsp: Chemin vers le fichier .tsp
        nb_stations_ring: Nombre de stations sur l'anneau
        
    Returns:
        Tuple (ring_indices, star_connections, cout_total)
    """
    # Charger l'instance
    probleme = chargerInstance(fichier_tsp)
    matrice_dist, noeuds = obtenirMatriceDistances(probleme)
    n = len(noeuds)
    
    print(f"Résolution Ring-Star (heuristique) pour {probleme.name} ({n} villes)")
    print(f"Nombre de stations sur le ring: {nb_stations_ring}")
    
    # Construire la solution ring-star avec heuristique
    ring_indices, star_connections, cout_total = construireRingStar(
        matrice_dist, noeuds, nb_stations_ring
    )
    
    # Convertir les indices en nœuds réels
    ring_noeuds = [noeuds[i] for i in ring_indices]
    star_noeuds = {noeuds[k]: noeuds[v] for k, v in star_connections.items()}
    
    print(f"\nSolution Ring-Star trouvée!")
    print(f"Ring ({len(ring_indices)} stations): {ring_noeuds}")
    print(f"Star connections ({len(star_connections)} stations):")
    for star, ring in star_noeuds.items():
        print(f"  Station {star} → Ring station {ring}")
    print(f"Coût total: {cout_total:.2f}")
    
    return ring_indices, star_connections, cout_total

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python heuristique.py <fichier.tsp> <nb_stations_ring>")
        print("Exemple: python heuristique.py data/ulysses16.tsp 5")
        sys.exit(1)
    
    fichier_tsp = sys.argv[1]
    nb_stations_ring = int(sys.argv[2])
    
    # Chercher le fichier dans différents emplacements possibles
    if not os.path.exists(fichier_tsp):
        # Essayer dans data/
        chemin_test = os.path.join("data", fichier_tsp)
        if os.path.exists(chemin_test):
            fichier_tsp = chemin_test
        else:
            # Essayer dans ../data/ (si on est dans src/)
            chemin_test = os.path.join("..", "data", fichier_tsp)
            if os.path.exists(chemin_test):
                fichier_tsp = chemin_test
    
    if not os.path.exists(fichier_tsp):
        print(f"Erreur: fichier {fichier_tsp} introuvable")
        sys.exit(1)
    
    ring_indices, star_connections, cout = resoudreRingStar_Heuristique(fichier_tsp, nb_stations_ring)

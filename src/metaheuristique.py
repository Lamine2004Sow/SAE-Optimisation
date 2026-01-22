import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import random
from instance import chargerInstance, obtenirMatriceDistances
from visualisation import construireRingStar

def calculerCout(chemin_indices, matrice_dist):
    """
    Calcule le coût total d'un chemin (cycle complet).
    
    Args:
        chemin_indices: Liste des indices des villes dans l'ordre
        matrice_dist: Matrice de distances
        
    Returns:
        Coût total du chemin
    """
    cout = sum(matrice_dist[chemin_indices[i]][chemin_indices[i+1]] 
               for i in range(len(chemin_indices)-1))
    cout += matrice_dist[chemin_indices[-1]][chemin_indices[0]]  # Retour au départ
    return cout

def voisin2opt(chemin_indices):
    """
    Génère un voisin en inversant une sous-séquence (mouvement 2-opt).
    
    Args:
        chemin_indices: Liste des indices des villes
        
    Returns:
        Nouveau chemin avec une inversion
    """
    n = len(chemin_indices)
    # Choisir deux positions aléatoirement (pas le premier ni le dernier)
    i, j = sorted(random.sample(range(1, n), 2))
    # Inverser la section entre i et j
    nouveau_chemin = chemin_indices[:i] + chemin_indices[i:j+1][::-1] + chemin_indices[j+1:]
    return nouveau_chemin

def recuitSimule(matrice_dist, solution_initiale, temp_initiale=1000.0, 
                 facteur_refroidissement=0.99, iterations_par_temp=100, 
                 temp_minimale=0.01):
    """
    Recuit simulé pour améliorer une solution TSP.
    
    Args:
        matrice_dist: Matrice de distances
        solution_initiale: Solution de départ (liste d'indices)
        temp_initiale: Température initiale
        facteur_refroidissement: Facteur de refroidissement (entre 0 et 1)
        iterations_par_temp: Nombre d'itérations à chaque température
        temp_minimale: Température minimale (critère d'arrêt)
        
    Returns:
        Tuple (meilleur_chemin_indices, meilleur_cout)
    """
    solution_courante = solution_initiale.copy()
    cout_courant = calculerCout(solution_courante, matrice_dist)
    
    meilleure_solution = solution_courante.copy()
    meilleur_cout = cout_courant
    
    temperature = temp_initiale
    iteration = 0
    
    while temperature > temp_minimale:
        for _ in range(iterations_par_temp):
            # Générer un voisin
            voisin = voisin2opt(solution_courante)
            cout_voisin = calculerCout(voisin, matrice_dist)
            
            # Calculer la différence de coût
            delta = cout_voisin - cout_courant
            
            # Accepter ou rejeter le voisin
            if delta < 0:
                # Amélioration: toujours accepter
                solution_courante = voisin
                cout_courant = cout_voisin
                
                # Mettre à jour la meilleure solution
                if cout_courant < meilleur_cout:
                    meilleure_solution = solution_courante.copy()
                    meilleur_cout = cout_courant
            else:
                # Dégradation: accepter avec probabilité exp(-delta/temperature)
                if random.random() < np.exp(-delta / temperature):
                    solution_courante = voisin
                    cout_courant = cout_voisin
        
        # Refroidir
        temperature *= facteur_refroidissement
        iteration += 1
        
        # Afficher la progression tous les 10 refroidissements
        if iteration % 10 == 0:
            print(f"Température: {temperature:.2f}, Meilleur coût: {meilleur_cout:.2f}")
    
    return meilleure_solution, meilleur_cout

def calculerCoutRingStar(ring_indices, star_connections, matrice_dist):
    """
    Calcule le coût total d'une solution ring-star.
    
    Args:
        ring_indices: Liste des indices des stations sur l'anneau (dans l'ordre)
        star_connections: Dict {station_star: station_ring}
        matrice_dist: Matrice de distances
        
    Returns:
        Coût total
    """
    # Coût du ring (cycle)
    cout_ring = 0
    for i in range(len(ring_indices)):
        cout_ring += matrice_dist[ring_indices[i]][ring_indices[(i+1) % len(ring_indices)]]
    
    # Coût des connexions star
    cout_star = sum(matrice_dist[star][ring] for star, ring in star_connections.items())
    
    return cout_ring + cout_star

def resoudreRingStar_Metaheuristique(fichier_tsp, nb_stations_ring):
    """
    Résout le problème Ring-Star avec une métaheuristique (recuit simulé).
    Commence par une solution heuristique puis améliore le ring avec recuit simulé.
    
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
    
    print(f"Résolution Ring-Star (métaheuristique) pour {probleme.name} ({n} villes)")
    print(f"Nombre de stations sur le ring: {nb_stations_ring}")
    
    # Obtenir une solution initiale avec heuristique
    ring_indices, star_connections, cout_initial = construireRingStar(
        matrice_dist, noeuds, nb_stations_ring
    )
    
    print(f"Solution initiale (heuristique): {cout_initial:.2f}")
    
    # Améliorer l'ordre du ring avec recuit simulé
    temp_initiale = 1000.0
    facteur_refroidissement = 0.995
    iterations_par_temp = max(50, len(ring_indices) // 2)
    
    print("Amélioration du ring avec recuit simulé...")
    ring_ameliore, cout_ring_ameliore = recuitSimule(
        matrice_dist,
        ring_indices,
        temp_initiale=temp_initiale,
        facteur_refroidissement=facteur_refroidissement,
        iterations_par_temp=iterations_par_temp,
        temp_minimale=0.01
    )
    
    # Recalculer les connexions star avec le nouveau ring
    stations_star = set(range(n)) - set(ring_ameliore)
    star_connections_ameliore = {}
    for station_star in stations_star:
        distances_vers_ring = [matrice_dist[station_star][ring_station] 
                               for ring_station in ring_ameliore]
        station_ring_proche = ring_ameliore[np.argmin(distances_vers_ring)]
        star_connections_ameliore[station_star] = station_ring_proche
    
    # Calculer le coût final
    cout_final = calculerCoutRingStar(ring_ameliore, star_connections_ameliore, matrice_dist)
    
    # Convertir les indices en nœuds réels
    ring_noeuds = [noeuds[i] for i in ring_ameliore]
    star_noeuds = {noeuds[k]: noeuds[v] for k, v in star_connections_ameliore.items()}
    
    print(f"\nSolution Ring-Star finale trouvée!")
    print(f"Ring ({len(ring_ameliore)} stations): {ring_noeuds}")
    print(f"Star connections ({len(star_connections_ameliore)} stations):")
    for star, ring in star_noeuds.items():
        print(f"  Station {star} → Ring station {ring}")
    print(f"Coût initial: {cout_initial:.2f}")
    print(f"Coût final: {cout_final:.2f}")
    print(f"Amélioration: {cout_initial - cout_final:.2f} ({((cout_initial - cout_final) / cout_initial * 100):.1f}%)")
    
    return ring_ameliore, star_connections_ameliore, cout_final

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python metaheuristique.py <fichier.tsp> <nb_stations_ring>")
        print("Exemple: python metaheuristique.py data/ulysses16.tsp 5")
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
    
    ring_indices, star_connections, cout = resoudreRingStar_Metaheuristique(fichier_tsp, nb_stations_ring)

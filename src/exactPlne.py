import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pulp
import numpy as np
from instance import chargerInstance, obtenirMatriceDistances

def resoudreRingStar_PLNE(fichier_tsp, nb_stations_ring, limite_temps=300):
    """
    Résout le problème Ring-Star avec une méthode exacte (PLNE).
    Sélectionne les stations pour le ring et optimise les connexions.
    
    Args:
        fichier_tsp: Chemin vers le fichier .tsp
        nb_stations_ring: Nombre de stations sur l'anneau
        limite_temps: Temps maximum en secondes pour la résolution
        
    Returns:
        Tuple (ring_indices, star_connections, cout_total) ou (None, None, None) si échec
    """
    # Charger l'instance
    probleme = chargerInstance(fichier_tsp)
    matrice_dist, noeuds = obtenirMatriceDistances(probleme)
    n = len(noeuds)
    nb_stations_ring = min(nb_stations_ring, n)
    
    print(f"Résolution Ring-Star (PLNE) pour {probleme.name} ({n} villes)")
    print(f"Nombre de stations sur le ring: {nb_stations_ring}")
    print(f"Limite de temps: {limite_temps} secondes")
    
    # Pour simplifier, on fixe les stations du ring (les premières nb_stations_ring)
    # et on optimise l'ordre du ring et les connexions star
    ring_stations = list(range(nb_stations_ring))
    star_stations = list(range(nb_stations_ring, n))
    
    # Créer le problème d'optimisation
    prob = pulp.LpProblem("RingStar", pulp.LpMinimize)
    
    # Variables pour le ring: x[i][j] = 1 si on va de i à j dans le ring
    x_ring = pulp.LpVariable.dicts("ring_arc", 
                                   [(i, j) for i in ring_stations 
                                    for j in ring_stations if i != j],
                                   cat='Binary')
    
    # Variables pour les connexions star: y[s][r] = 1 si station star s est connectée à ring r
    y_star = pulp.LpVariable.dicts("star_arc",
                                    [(s, r) for s in star_stations 
                                     for r in ring_stations],
                                    cat='Binary')
    
    # Variables u pour contraintes MTZ du ring
    u = pulp.LpVariable.dicts("u", ring_stations, lowBound=0, upBound=nb_stations_ring-1, cat='Integer')
    
    # Fonction objectif: minimiser coût ring + coût star
    cout_ring = pulp.lpSum([matrice_dist[i][j] * x_ring[(i, j)] 
                           for i in ring_stations for j in ring_stations if i != j])
    cout_star = pulp.lpSum([matrice_dist[s][r] * y_star[(s, r)] 
                           for s in star_stations for r in ring_stations])
    prob += cout_ring + cout_star
    
    # Contraintes ring: chaque station du ring a exactement un successeur
    for i in ring_stations:
        prob += pulp.lpSum([x_ring[(i, j)] for j in ring_stations if i != j]) == 1
    
    # Contraintes ring: chaque station du ring a exactement un prédécesseur
    for j in ring_stations:
        prob += pulp.lpSum([x_ring[(i, j)] for i in ring_stations if i != j]) == 1
    
    # Contraintes MTZ pour éviter les sous-tours dans le ring
    for i in ring_stations[1:]:
        for j in ring_stations[1:]:
            if i != j:
                prob += u[i] - u[j] + nb_stations_ring * x_ring[(i, j)] <= nb_stations_ring - 1
    
    # Contraintes star: chaque station star est connectée à exactement une station ring
    for s in star_stations:
        prob += pulp.lpSum([y_star[(s, r)] for r in ring_stations]) == 1
    
    # Résoudre le problème
    print("Résolution en cours...")
    prob.solve(pulp.PULP_CBC_CMD(timeLimit=limite_temps, msg=1))
    
    # Vérifier le statut de la résolution
    status = pulp.LpStatus[prob.status]
    print(f"Statut: {status}")
    
    if status == 'Optimal':
        # Extraire l'ordre du ring
        ring_ordre = [ring_stations[0]]
        actuel = ring_stations[0]
        
        while len(ring_ordre) < nb_stations_ring:
            for j in ring_stations:
                if j != actuel and pulp.value(x_ring[(actuel, j)]) == 1:
                    ring_ordre.append(j)
                    actuel = j
                    break
        
        # Extraire les connexions star
        star_connections = {}
        for s in star_stations:
            for r in ring_stations:
                if pulp.value(y_star[(s, r)]) == 1:
                    star_connections[s] = r
                    break
        
        # Calculer le coût total
        cout_ring_val = sum(matrice_dist[ring_ordre[i]][ring_ordre[(i+1) % len(ring_ordre)]] 
                           for i in range(len(ring_ordre)))
        cout_star_val = sum(matrice_dist[s][r] for s, r in star_connections.items())
        cout_total = cout_ring_val + cout_star_val
        
        # Convertir en nœuds réels
        ring_noeuds = [noeuds[i] for i in ring_ordre]
        star_noeuds = {noeuds[k]: noeuds[v] for k, v in star_connections.items()}
        
        print(f"\nSolution optimale trouvée!")
        print(f"Ring ({len(ring_ordre)} stations): {ring_noeuds}")
        print(f"Star connections ({len(star_connections)} stations):")
        for star, ring in star_noeuds.items():
            print(f"  Station {star} → Ring station {ring}")
        print(f"Coût total: {cout_total:.2f}")
        
        return ring_ordre, star_connections, cout_total
    else:
        print(f"Pas de solution optimale trouvée (statut: {status})")
        return None, None, None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python exactPlne.py <fichier.tsp> <nb_stations_ring> [limite_temps]")
        print("Exemple: python exactPlne.py data/ulysses16.tsp 5 300")
        sys.exit(1)
    
    fichier_tsp = sys.argv[1]
    nb_stations_ring = int(sys.argv[2])
    limite_temps = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    
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
    
    ring_indices, star_connections, cout = resoudreRingStar_PLNE(fichier_tsp, nb_stations_ring, limite_temps)

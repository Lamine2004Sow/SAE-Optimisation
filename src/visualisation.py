import sys
import os

# Ajouter le répertoire src au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import matplotlib.pyplot as plt
from instance import chargerInstance, obtenirMatriceDistances

def construireRingStar(matrice_dist, noeuds, nb_stations_ring):
    """
    Construit une solution ring-star :
    - Ring : cycle avec nb_stations_ring stations
    - Star : les autres stations sont connectées au ring
    
    Args:
        matrice_dist: Matrice de distances
        noeuds: Liste des nœuds
        nb_stations_ring: Nombre de stations sur l'anneau
        
    Returns:
        Tuple (ring_indices, star_connections, cout_total)
        ring_indices: Liste des indices des stations sur l'anneau (dans l'ordre du cycle)
        star_connections: Dict {station_star: station_ring} pour les connexions étoile
        cout_total: Coût total de la solution
    """
    n = len(noeuds)
    nb_stations_ring = min(nb_stations_ring, n)  # Ne pas dépasser le nombre total
    
    # Sélectionner les stations pour le ring (les premières stations)
    ring_indices = list(range(nb_stations_ring))
    
    # Construire le cycle du ring (ordre optimal avec plus proche voisin)
    ring_ordre = [ring_indices[0]]
    ring_restant = set(ring_indices[1:])
    
    while ring_restant:
        actuel = ring_ordre[-1]
        distances = [matrice_dist[actuel][i] if i in ring_restant else np.inf 
                     for i in range(n)]
        prochain = np.argmin(distances)
        ring_ordre.append(prochain)
        ring_restant.remove(prochain)
    
    # Calculer le coût du ring
    cout_ring = 0
    for i in range(len(ring_ordre)):
        cout_ring += matrice_dist[ring_ordre[i]][ring_ordre[(i+1) % len(ring_ordre)]]
    
    # Connecter les stations restantes en étoile vers le ring
    star_connections = {}
    cout_star = 0
    stations_star = set(range(n)) - set(ring_ordre)
    
    for station_star in stations_star:
        # Trouver la station du ring la plus proche
        distances_vers_ring = [matrice_dist[station_star][ring_station] 
                               for ring_station in ring_ordre]
        station_ring_proche = ring_ordre[np.argmin(distances_vers_ring)]
        star_connections[station_star] = station_ring_proche
        cout_star += matrice_dist[station_star][station_ring_proche]
    
    cout_total = cout_ring + cout_star
    
    return ring_ordre, star_connections, cout_total

def visualiserRingStar(probleme, ring_indices, star_connections, noeuds, titre="Solution Ring-Star"):
    """
    Visualise une solution ring-star avec l'anneau et les étoiles.
    
    Args:
        probleme: Instance TSP chargée
        ring_indices: Liste des indices des stations sur l'anneau
        star_connections: Dict {station_star: station_ring}
        noeuds: Liste des nœuds
        titre: Titre du graphique
    """
    coords = probleme.node_coords
    if not coords:
        print("⚠️  Pas de coordonnées disponibles pour cette instance")
        return
    
    # Créer la figure
    plt.figure(figsize=(14, 10))
    
    # Extraire les coordonnées
    x_coords = {}
    y_coords = {}
    for i, node in enumerate(noeuds):
        if node in coords:
            x_coords[i] = coords[node][0]
            y_coords[i] = coords[node][1]
    
    # Dessiner le RING (anneau) en bleu
    ring_x = [x_coords[i] for i in ring_indices]
    ring_y = [y_coords[i] for i in ring_indices]
    # Fermer le cycle
    ring_x.append(ring_x[0])
    ring_y.append(ring_y[0])
    
    plt.plot(ring_x, ring_y, 'b-', linewidth=3, alpha=0.7, label='Ring (Anneau)', zorder=2)
    plt.scatter(ring_x[:-1], ring_y[:-1], c='blue', s=200, zorder=5, edgecolors='darkblue', linewidths=2)
    
    # Annoter les stations du ring
    for i, idx in enumerate(ring_indices):
        plt.annotate(f'R{noeuds[idx]}', (x_coords[idx], y_coords[idx]), 
                    fontsize=10, ha='center', va='center', 
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.7),
                    fontweight='bold')
    
    # Dessiner les STAR (étoiles) en rouge
    for station_star, station_ring in star_connections.items():
        x1, y1 = x_coords[station_star], y_coords[station_star]
        x2, y2 = x_coords[station_ring], y_coords[station_ring]
        plt.plot([x1, x2], [y1, y2], 'r--', linewidth=1.5, alpha=0.5, zorder=1)
        plt.scatter(x1, y1, c='red', s=150, zorder=4, edgecolors='darkred', linewidths=1.5)
        # Annoter les stations star
        plt.annotate(f'S{noeuds[station_star]}', (x1, y1), 
                    fontsize=9, ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.7))
    
    plt.title(titre, fontsize=16, fontweight='bold')
    plt.xlabel('X', fontsize=12)
    plt.ylabel('Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11, loc='best')
    plt.tight_layout()
    
    # Sauvegarder
    img_dir = "img"
    if not os.path.exists(img_dir):
        if os.path.exists(os.path.join("..", "img")):
            img_dir = os.path.join("..", "img")
        else:
            os.makedirs(img_dir, exist_ok=True)
    
    img_path = os.path.join(img_dir, f"{probleme.name}_ringstar.png")
    plt.savefig(img_path, dpi=150, bbox_inches='tight')
    print(f"Visualisation sauvegardée: {img_path}")
    plt.show()
    plt.close()

def resoudreRingStar(fichier_tsp, nb_stations_ring):
    """
    Résout le problème ring-star et visualise la solution.
    
    Args:
        fichier_tsp: Chemin vers le fichier .tsp
        nb_stations_ring: Nombre de stations sur l'anneau
    """
    # Charger l'instance
    probleme = chargerInstance(fichier_tsp)
    matrice_dist, noeuds = obtenirMatriceDistances(probleme)
    n = len(noeuds)
    
    print(f"Résolution Ring-Star pour {probleme.name} ({n} villes)")
    print(f"Nombre de stations sur le ring: {nb_stations_ring}")
    
    # Construire la solution ring-star
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
    
    # Visualiser
    visualiserRingStar(probleme, ring_indices, star_connections, noeuds, 
                      f"Solution Ring-Star ({nb_stations_ring} stations sur ring)")
    
    return ring_indices, star_connections, cout_total

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python visualisation.py <fichier.tsp> <nb_stations_ring>")
        print("Exemple: python visualisation.py data/ulysses16.tsp 5")
        sys.exit(1)
    
    fichier_tsp = sys.argv[1]
    nb_stations_ring = int(sys.argv[2])
    
    # Chercher le fichier dans différents emplacements possibles
    if not os.path.exists(fichier_tsp):
        chemin_test = os.path.join("data", fichier_tsp)
        if os.path.exists(chemin_test):
            fichier_tsp = chemin_test
        else:
            chemin_test = os.path.join("..", "data", fichier_tsp)
            if os.path.exists(chemin_test):
                fichier_tsp = chemin_test
    
    if not os.path.exists(fichier_tsp):
        print(f"Erreur: fichier {fichier_tsp} introuvable")
        sys.exit(1)
    
    resoudreRingStar(fichier_tsp, nb_stations_ring)

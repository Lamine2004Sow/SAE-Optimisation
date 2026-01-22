import tsplib95 as tsp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Fonction pour charger une instance de TSP
def chargerInstance(fichier):
    probleme = tsp.load(fichier)
    return probleme

# Fonction pour créer le graphe de l'instance
def creerGraphe(probleme):
    g = probleme.get_graph()
    return g

# Fonction pour afficher le graphe
def afficherGraphe(graphe, probleme):
    coords = probleme.node_coords
    pos = {}
    if coords:
        # Utilise les coordonnées de l'instance quand elles existent
        for node in graphe.nodes():
            if node in coords:
                pos[node] = coords[node]

    if len(pos) != len(graphe.nodes()):
        pos = nx.spring_layout(graphe, seed=4)

    nx.draw(graphe, pos, with_labels=True)
    
    # Créer le répertoire img/ s'il n'existe pas
    img_dir = "img"
    if not os.path.exists(img_dir):
        # Essayer aussi ../img/ si on est dans src/
        if os.path.exists(os.path.join("..", "img")):
            img_dir = os.path.join("..", "img")
        else:
            os.makedirs(img_dir, exist_ok=True)
    
    img_path = os.path.join(img_dir, probleme.name + ".png")
    plt.savefig(img_path)
    print(f"Graphe sauvegardé: {img_path}")
    plt.show()
    plt.close()


# Fonction pour obtenir la matrice de distances
def obtenirMatriceDistances(probleme):
    """
    Retourne la matrice de distances sous forme de numpy array.
    Utilise le graphe pour obtenir les distances si disponibles,
    sinon calcule à partir des coordonnées.
    """
    graphe = creerGraphe(probleme)
    noeuds = sorted(graphe.nodes())
    n = len(noeuds)
    
    # Créer la matrice numpy
    matriceDist = np.zeros((n, n))
    
    for i, node_i in enumerate(noeuds):
        for j, node_j in enumerate(noeuds):
            if i == j:
                matriceDist[i][j] = 0
            else:
                # Utiliser le poids de l'arête du graphe
                if graphe.has_edge(node_i, node_j):
                    matriceDist[i][j] = graphe[node_i][node_j].get('weight', 0)
                else:
                    # Si pas d'arête, calculer depuis les coordonnées
                    coords = probleme.node_coords
                    if coords and node_i in coords and node_j in coords:
                        xi, yi = coords[node_i]
                        xj, yj = coords[node_j]
                        matriceDist[i][j] = np.sqrt((xi - xj)**2 + (yi - yj)**2)
    
    return matriceDist, noeuds
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python instance.py <fichier.tsp>")
        sys.exit(1)
    
    fichier_tsp = sys.argv[1]
    
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
    
    probleme = chargerInstance(fichier_tsp)
    print(f"Instance chargée: {probleme.name}")
    print(f"Dimension: {probleme.dimension}")
    
    graphe = creerGraphe(probleme)
    print(f"Graphe créé: {graphe.number_of_nodes()} nœuds, {graphe.number_of_edges()} arêtes")
    
    matriceDistances, noeuds = obtenirMatriceDistances(probleme)
    print(f"Matrice de distances: {matriceDistances.shape}")
    print(f"Première ligne: {matriceDistances[0, :5]}")
import tsplib95 as tsp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pulp
import random
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
    nx.draw(graphe, coords,with_labels=True)
    plt.savefig("img/"+probleme.name+".png")
    plt.show()
    plt.close()


# Fonction pour obtenir la matrice de distances
def obtenirMatriceDistances(probleme):

    coords = probleme.node_coords
    noeuds = list(coords.keys())

    matriceDist = {i: {} for i in noeuds}

    for i in noeuds:
        xi, yi = coords[i]
        for j in noeuds:
            if i == j:
                matriceDist[i][j] = 0
            else:
                xj, yj = coords[j]
                matriceDist[i][j] = np.sqrt((xi - xj)**2 + (yi - yj)**2)

    return matriceDist

if __name__ == "__main__":
    probleme = chargerInstance("data/ulysses16.tsp")
    graphe = creerGraphe(probleme)
    afficherGraphe(graphe, probleme)
    matriceDistances = obtenirMatriceDistances(probleme)
    print(matriceDistances)
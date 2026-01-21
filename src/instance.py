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
def afficherGraphe(graphe):
    nx.draw(graphe, with_labels=True)
    plt.show()

# Fonction pour obtenir la matrice de distances
def obtenirMatriceDistances(probleme):

    coords = probleme.node_coords
    neuds = list(coords.keys())

    maticeDist = {}

    for i in neuds:
        for j in neuds:
            if i == j:
                maticeDist[i, j] = 0
            else:
                xi, yi = coords[i]
                xj, yj = coords[j]
                maticeDist[i, j] = np.sqrt((xi - xj)**2 + (yi - yj)**2)

    return maticeDist

if __name__ == "__main__":
    probleme = chargerInstance("data/ulysses16.tsp")
    graphe = creerGraphe(probleme)
    afficherGraphe(graphe)
    matriceDistances = obtenirMatriceDistances(probleme)
    print(matriceDistances)
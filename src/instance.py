import tsplib95 as tsp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
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
def obtenirMatriceDistances(graphe):
    return nx.to_numpy_array(graphe)




if __name__ == "__main__":
    probleme = chargerInstance(sys.argv[1])
    print(probleme.render())
    graphe = creerGraphe(probleme)
    afficherGraphe(graphe) 

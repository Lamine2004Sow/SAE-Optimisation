import tsplib95 as tsp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pulp
import random
import sys
import math
import os

# Fonction pour charger l'instance
def chargerInstance(fichier):
    probleme = tsp.load(fichier)
    return probleme

# Fonction pour créer le graphe
def creerGraphe(probleme):
    g = probleme.get_graph()
    return g

# Fonction pour obtenir la matrice de distances
def obtenirMatriceDistances(probleme):

    coords = probleme.node_coords
    noeuds = sorted(list(coords.keys()))
    n = len(noeuds)

    indexNoeud = {i: noeuds[i] for i in range(n)}
    noeudIndex = {noeuds[i]: i for i in range(n)}

    matrice = np.zeros((n, n))

    for i in range(n):
        ni = indexNoeud[i]
        xi, yi = coords[ni]
        for j in range(n):
            nj = indexNoeud[j]
            if i == j:
                matrice[i][j] = 0
            else:
                xj, yj = coords[nj]
                matrice[i][j] = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

    return matrice, indexNoeud, noeudIndex

# Fonction pour afficher le graphe
def afficherGraphe(probleme):
    g = creerGraphe(probleme)
    coords = probleme.node_coords

    positions = {noeud: coords[noeud] for noeud in g.nodes()}

    nx.draw(g, positions, with_labels=True)
    plt.savefig(f"img/{probleme.name}.png")
    plt.show()
    plt.close()

# Fonction pour trouver la station la plus proche
def plusProcheStation(probleme, clients, stations):
    matrice, indexNoeud, noeudIndex = obtenirMatriceDistances(probleme)

    ligneEtoile = []

    for c in clients:
        i = noeudIndex[c]
        mStation = stations[0]
        mDist = matrice[i][noeudIndex[mStation]]
        for s in stations[1:]:
            dist = matrice[i][noeudIndex[s]]
            if dist < mDist:
                mDist = dist
                mStation = s
        ligneEtoile.append((c, mStation))
    return ligneEtoile

# Fontion pour construire le graphe
def construireGraphe(probleme, cycle, stations):
    g = creerGraphe(probleme)
    coords = probleme.node_coords

    #aretes du metro
    ligneMetro = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
    g.add_edges_from(ligneMetro)

    #aretes des etoiles
    clients = [n for n in coords if n not in stations]
    ligneEtoile = plusProcheStation(probleme, clients, stations)
    g.add_edges_from(ligneEtoile)
    return g, ligneMetro, ligneEtoile


# Fonction pour dessiner le graphe
def dessinerGraphe(graphe, probleme, stations, ligneMetro, ligneEtoile, methode="solution"):
    coords = probleme.node_coords
    pos = {node: (x, y) for node, (x, y) in coords.items()}

    clients = [n for n in coords if n not in stations]

    plt.figure(figsize=(20, 20))

    # Noeuds
    nx.draw_networkx_nodes(graphe, pos, nodelist=stations, node_color="red", node_size=100)
    nx.draw_networkx_nodes(graphe, pos, nodelist=clients, node_color="blue", node_size=50)

    # Arêtes
    nx.draw_networkx_edges(graphe, pos, edgelist=ligneMetro, width=2, edge_color="red")
    nx.draw_networkx_edges(graphe, pos, edgelist=ligneEtoile, width=1, edge_color="gray", style="dotted")

    # Labels
    nx.draw_networkx_labels(graphe, pos, font_size=8)

    plt.axis("equal")
    plt.title(f"Solution {methode} - {probleme.name}")

    # Créer dossier img si nécessaire
    os.makedirs("img", exist_ok=True)
    nom_fichier = f"img/Solution_{methode}_{probleme.name}.png"
    plt.savefig(nom_fichier, dpi=150, bbox_inches='tight')
    print(f"Schéma sauvegardé : {nom_fichier}")

    plt.show()
    plt.close()

# Fonction pour afficher la solution
def afficherSolution(probleme, cycle, stations, methode="solution"):
    graphe, ligneMetro, ligneEtoile = construireGraphe(probleme, cycle, stations)
    dessinerGraphe(graphe, probleme, stations, ligneMetro, ligneEtoile, methode)


from instance import *
import pulp
import sys

def resolutionExactPlne(fichier, p):
    pb = chargerInstance(fichier)
    graphe = creerGraphe(pb)
    afficherGraphe(graphe)

    V = list(graphe.nodes())
    E = list(graphe.edges())

    p = int(p)


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
    pos = {}
    if coords:
        # Utilise les coordonnées de l'instance quand elles existent
        for node in graphe.nodes():
            if node in coords:
                pos[node] = coords[node]

    if len(pos) != len(graphe.nodes()):
        pos = nx.spring_layout(graphe, seed=4)

    nx.draw(graphe, pos, with_labels=True)
    plt.savefig(f"img/{probleme.name}.png")
    plt.show()
    plt.close()


# Fonction pour obtenir la matrice de distances
def obtenirMatriceDistances(probleme):

    coords = probleme.node_coords
    noeuds = sorted(list(coords.keys()))
    n = len(noeuds)

    # Dictionnaires utiles pour passer d'un index à un numéro de noeud et inversement
    index_to_node = {i: noeuds[i] for i in range(n)}
    node_to_index = {noeuds[i]: i for i in range(n)}

    matrice = np.zeros((n, n))

    for i in range(n):
        ni = index_to_node[i]
        xi, yi = coords[ni]
        for j in range(n):
            nj = index_to_node[j]
            if i == j:
                matrice[i][j] = 0
            else:
                xj, yj = coords[nj]
                matrice[i][j] = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)

    return matrice, index_to_node, node_to_index


# Affichage d'une solution anneau + étoiles
def afficherSolution(probleme, cycle, stations):
    coords = probleme.node_coords
    pos = {node: (x, y) for node, (x, y) in coords.items()}
    graphe = nx.Graph()

    # Ajout des noeuds
    for node in coords.keys():
        graphe.add_node(node)

    # Arêtes de l'anneau (métro)
    edges_metro = []
    p = len(cycle)
    for k in range(p):
        u = cycle[k]
        v = cycle[(k + 1) % p]
        graphe.add_edge(u, v)
        edges_metro.append((u, v))

    # Arêtes des étoiles (clients -> station la plus proche)
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    clients = [n for n in coords.keys() if n not in stations]
    edges_etoiles = []
    for c in clients:
        i = node_to_index[c]
        best_station = None
        best_dist = float("inf")
        for s in stations:
            j = node_to_index[s]
            d = matrice[i][j]
            if d < best_dist:
                best_dist = d
                best_station = s
        graphe.add_edge(c, best_station)
        edges_etoiles.append((c, best_station))

    plt.figure()
    nx.draw_networkx_nodes(graphe, pos, nodelist=stations, node_color="red")
    nx.draw_networkx_nodes(graphe, pos, nodelist=clients, node_color="blue", node_size=50)
    nx.draw_networkx_edges(graphe, pos, edgelist=edges_metro, width=2, edge_color="red", style="solid")
    nx.draw_networkx_edges(graphe, pos, edgelist=edges_etoiles, width=1, edge_color="gray", style="dotted")
    nx.draw_networkx_labels(graphe, pos, font_size=8)
    plt.axis("equal")
    plt.show()
    plt.close()


# =========================
# Brique B : heuristique rapide
# =========================
def choisirStations_aleatoire(probleme, p):
    noeuds = list(probleme.node_coords.keys())
    return random.sample(noeuds, p)


def tsp_plus_proche_voisin(matrice, stations, node_to_index):
    non_visites = set(stations)
    courant = stations[0]
    cycle = [courant]
    non_visites.remove(courant)

    while non_visites:
        i = node_to_index[courant]
        meilleur = None
        best_dist = float("inf")
        for s in non_visites:
            j = node_to_index[s]
            d = matrice[i][j]
            if d < best_dist:
                best_dist = d
                meilleur = s
        cycle.append(meilleur)
        non_visites.remove(meilleur)
        courant = meilleur

    return cycle


def heuristique_rapide(probleme, p):
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    stations = choisirStations_aleatoire(probleme, p)
    cycle = tsp_plus_proche_voisin(matrice, stations, node_to_index)
    return cycle, stations


# =========================
# Brique C : amélioration locale
# =========================
def cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index):
    if not stations or not cycle:
        return float('inf')
    
    cout_anneau = 0.0
    p = len(cycle)
    for k in range(p):
        u = cycle[k]
        v = cycle[(k + 1) % p]
        cout_anneau += matrice[node_to_index[u]][node_to_index[v]]

    coords = probleme.node_coords
    clients = [n for n in coords if n not in stations]
    cout_etoiles = 0.0
    for c in clients:
        i = node_to_index[c]
        best = min(matrice[i][node_to_index[s]] for s in stations)
        cout_etoiles += best

    return cout_anneau + cout_etoiles


def amelioration_locale(probleme, p, cycle_init, stations_init, max_iter=100):
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cycle = cycle_init[:]
    stations = stations_init[:]
    cout_actuel = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)

    coords = probleme.node_coords
    tous = list(coords.keys())

    for _ in range(max_iter):
        amelioration = False
        for s in stations:
            for c in tous:
                if c in stations:
                    continue
                nouvelles_stations = stations[:]
                nouvelles_stations.remove(s)
                nouvelles_stations.append(c)

                nouveau_cycle = tsp_plus_proche_voisin(matrice, nouvelles_stations, node_to_index)
                cout_new = cout_solution(
                    probleme, nouveau_cycle, nouvelles_stations, matrice, index_to_node, node_to_index
                )

                if cout_new < cout_actuel:
                    stations = nouvelles_stations
                    cycle = nouveau_cycle
                    cout_actuel = cout_new
                    amelioration = True
                    break
            if amelioration:
                break
        if not amelioration:
            break

    return cycle, stations, cout_actuel


# =========================
# Brique D : méthode exacte (PLNE)
# =========================
def reconstruire_cycle_depuis_arcs(edges_metro, stations):
    succ = {s: None for s in stations}
    for (i, j) in edges_metro:
        if i in succ:
            succ[i] = j

    if not stations:
        return []

    start = stations[0]
    cycle = [start]
    courant = start
    while True:
        suivant = succ.get(courant)
        if suivant is None or suivant == start:
            break
        cycle.append(suivant)
        courant = suivant

    return cycle


def methode_exacte(probleme, p):
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    noeuds = list(index_to_node.values())
    n = len(noeuds)

    model = pulp.LpProblem("RingStar", pulp.LpMinimize)

    # Variables
    x = pulp.LpVariable.dicts("x", (noeuds, noeuds), 0, 1, cat="Binary")  # arêtes orientées de l'anneau
    z = pulp.LpVariable.dicts("z", noeuds, 0, 1, cat="Binary")  # station ou non
    y = pulp.LpVariable.dicts("y", (noeuds, noeuds), 0, 1, cat="Binary")  # affectation client -> station
    u = pulp.LpVariable.dicts("u", noeuds, lowBound=0, upBound=n, cat="Continuous")  # MTZ

    # Objectif : coût anneau + coût étoiles
    cout_anneau = pulp.lpSum(
        matrice[node_to_index[i]][node_to_index[j]] * x[i][j] for i in noeuds for j in noeuds if i != j
    )
    cout_etoiles = pulp.lpSum(
        matrice[node_to_index[i]][node_to_index[j]] * y[i][j] for i in noeuds for j in noeuds
    )
    model += cout_anneau + cout_etoiles

    # 1) nombre de stations = p
    model += pulp.lpSum(z[i] for i in noeuds) == p

    # 2) affectation unique de chaque noeud à une station
    for i in noeuds:
        model += pulp.lpSum(y[i][j] for j in noeuds) == 1

    # 3) affectation seulement si j est station
    for i in noeuds:
        for j in noeuds:
            model += y[i][j] <= z[j]

    # 4) contraintes d'anneau : degré entrant = 1 et sortant = 1 pour les stations, 0 sinon
    for i in noeuds:
        model += pulp.lpSum(x[i][j] for j in noeuds if i != j) == z[i]
        model += pulp.lpSum(x[j][i] for j in noeuds if i != j) == z[i]

    # 5) l'arête ne peut exister que si les deux sont stations
    for i in noeuds:
        for j in noeuds:
            if i == j:
                model += x[i][j] == 0
            else:
                model += x[i][j] <= z[i]
                model += x[i][j] <= z[j]

    # 6) élimination des sous-tours (MTZ) sur les stations
    #    u est défini pour tous les noeuds mais activé seulement si z=1
    for i in noeuds:
        model += u[i] <= p * z[i]
        model += u[i] >= z[i]  # u[i] >= 1 si z[i] = 1, sinon u[i] >= 0
    
    # Contrainte MTZ : u[i] - u[j] + p*x[i][j] <= p - 1
    # Cette contrainte s'applique seulement quand x[i][j] = 1
    for i in noeuds:
        for j in noeuds:
            if i != j:
                # Si x[i][j] = 1, alors u[i] - u[j] <= -1, ce qui force un ordre
                model += u[i] - u[j] + p * x[i][j] <= p - 1

    # Résolution
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # Vérifier le statut de la résolution
    status = model.status
    if status != pulp.LpStatusOptimal:
        print(f"Attention : Le solveur n'a pas trouvé de solution optimale. Statut : {pulp.LpStatus[status]}")
        print("Retour à une solution heuristique...")
        # Fallback : utiliser l'heuristique
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations

    stations = [i for i in noeuds if pulp.value(z[i]) is not None and pulp.value(z[i]) > 0.5]

    if not stations:
        print("Attention : Aucune station trouvée dans la solution. Retour à une solution heuristique...")
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations

    edges_metro = []
    for i in noeuds:
        for j in noeuds:
            if i != j and pulp.value(x[i][j]) is not None and pulp.value(x[i][j]) > 0.5:
                edges_metro.append((i, j))

    cycle = reconstruire_cycle_depuis_arcs(edges_metro, stations)
    
    if not cycle:
        print("Attention : Cycle vide. Retour à une solution heuristique...")
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations
    
    return cycle, stations


# Petit main de test
def main():
    fichier = "data/ulysses16.tsp"
    p = 4

    probleme = chargerInstance(fichier)

    # Heuristique rapide
    cycle_h, stations_h = heuristique_rapide(probleme, p)
    afficherSolution(probleme, cycle_h, stations_h)

    # Amélioration locale
    cycle_c, stations_c, cout_c = amelioration_locale(probleme, p, cycle_h, stations_h)
    afficherSolution(probleme, cycle_c, stations_c)

    # Méthode exacte (attention plus lente)
    cycle_d, stations_d = methode_exacte(probleme, p)
    afficherSolution(probleme, cycle_d, stations_d)


if __name__ == "__main__":
    main()

import tsplib95 as tsp
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pulp
import random
import sys
import math
import os

# Fonction pour charger une instance de TSP
def chargerInstance(fichier):
    probleme = tsp.load(fichier)
    return probleme

# Fonction pour calculer automatiquement le nombre de stations K
# Formule : K = max(3, ⌈√n⌉) où n est le nombre de nœuds
# Cela garantit K >= 3 et est proportionnel à la taille de l'instance
def calculerNombreStations(probleme):
    n = len(probleme.node_coords)
    k = max(3, math.ceil(math.sqrt(n)))
    return k

# Fonction pour créer le graphe de l'instance
def creerGraphe(probleme):
    g = probleme.get_graph()
    return g

# Fonction pour afficher le nuage de points (sans solution)
def afficherNuagePoints(probleme):
    """
    Affiche simplement le nuage de points de l'instance TSP.
    Utile pour visualiser les données avant résolution.
    """
    coords = probleme.node_coords
    if not coords:
        print("⚠️  Pas de coordonnées disponibles pour cette instance")
        return
    
    # Extraire les coordonnées
    x_coords = [coords[node][0] for node in coords.keys()]
    y_coords = [coords[node][1] for node in coords.keys()]
    
    plt.figure(figsize=(10, 8))
    plt.scatter(x_coords, y_coords, c='blue', s=50, alpha=0.6)
    
    # Annoter les points avec leur numéro
    for node, (x, y) in coords.items():
        plt.annotate(str(node), (x, y), fontsize=8, ha='center', va='center')
    
    plt.title(f"Nuage de points - {probleme.name}")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True, alpha=0.3)
    plt.axis("equal")
    
    # Créer le dossier img/ s'il n'existe pas
    os.makedirs("img", exist_ok=True)
    
    # Sauvegarder l'image
    nom_fichier = f"img/NuagePoints_{probleme.name}.png"
    plt.savefig(nom_fichier, dpi=150, bbox_inches='tight')
    print(f"Nuage de points sauvegardé : {nom_fichier}")
    
    plt.show()
    plt.close()


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
def afficherSolution(probleme, cycle, stations, methode="solution"):
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

    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(graphe, pos, nodelist=stations, node_color="red", node_size=100)
    nx.draw_networkx_nodes(graphe, pos, nodelist=clients, node_color="blue", node_size=50)
    nx.draw_networkx_edges(graphe, pos, edgelist=edges_metro, width=2, edge_color="red", style="solid")
    nx.draw_networkx_edges(graphe, pos, edgelist=edges_etoiles, width=1, edge_color="gray", style="dotted")
    nx.draw_networkx_labels(graphe, pos, font_size=8)
    plt.axis("equal")
    plt.title(f"Solution {methode} - {probleme.name}")
    
    # Créer le dossier img/ s'il n'existe pas
    os.makedirs("img", exist_ok=True)
    
    # Sauvegarder l'image
    nom_fichier = f"img/Solution_{methode}_{probleme.name}.png"
    plt.savefig(nom_fichier, dpi=150, bbox_inches='tight')
    print(f"Schéma sauvegardé : {nom_fichier}")
    
    plt.show()
    plt.close()


# =========================
# Brique B : heuristique rapide
# =========================
def choisirStations_aleatoire(probleme, p):
    """
    Choisit p stations aléatoirement parmi tous les nœuds.
    IMPORTANT : Le sommet 1 (ou le premier sommet) est TOUJOURS une station.
    """
    noeuds = list(probleme.node_coords.keys())
    # Le premier sommet (1 ou 0 selon la numérotation) est toujours une station
    premier_sommet = noeuds[0]
    autres_noeuds = [n for n in noeuds if n != premier_sommet]
    # Choisir p-1 stations parmi les autres
    autres_stations = random.sample(autres_noeuds, min(p - 1, len(autres_noeuds)))
    return [premier_sommet] + autres_stations


def tsp_plus_proche_voisin(matrice, stations, node_to_index):
    """
    Construit un cycle (anneau) sur les stations en utilisant l'heuristique 
    du plus proche voisin.
    IMPORTANT : Le cycle commence toujours par le premier sommet (station 1).
    """
    if not stations:
        return []
    
    # Le premier sommet (station 1) doit être le point de départ
    premier_sommet = stations[0]
    non_visites = set(stations)
    courant = premier_sommet
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
    """
    Heuristique rapide pour Ring-Star :
    1. Choisit p stations aléatoirement
    2. Construit un cycle sur ces stations (plus proche voisin)
    3. Les clients sont automatiquement affectés à la station la plus proche
    """
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    stations = choisirStations_aleatoire(probleme, p)
    cycle = tsp_plus_proche_voisin(matrice, stations, node_to_index)
    return cycle, stations


# =========================
# Brique C : amélioration locale
# =========================
def cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index):
    """
    Calcule le coût total d'une solution Ring-Star :
    - Coût de l'anneau (cycle entre stations)
    - Coût des étoiles (distance de chaque client à sa station la plus proche)
    """
    if not stations or not cycle:
        return float('inf')
    
    # Coût de l'anneau : somme des distances entre stations consécutives
    cout_anneau = 0.0
    p = len(cycle)
    for k in range(p):
        u = cycle[k]
        v = cycle[(k + 1) % p]
        cout_anneau += matrice[node_to_index[u]][node_to_index[v]]

    # Coût des étoiles : chaque client est affecté à la station la plus proche
    coords = probleme.node_coords
    clients = [n for n in coords if n not in stations]
    cout_etoiles = 0.0
    for c in clients:
        i = node_to_index[c]
        best = min(matrice[i][node_to_index[s]] for s in stations)
        cout_etoiles += best

    return cout_anneau + cout_etoiles


def amelioration_locale(probleme, p, cycle_init, stations_init, max_iter=100):
    """
    Amélioration locale par échange de stations :
    - Pour chaque station (SAUF le premier sommet), teste de la remplacer par un client
    - Garde l'amélioration si elle réduit le coût
    - S'arrête quand plus d'amélioration possible ou max_iter atteint
    IMPORTANT : Le premier sommet reste toujours une station.
    """
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cycle = cycle_init[:]
    stations = stations_init[:]
    cout_actuel = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)

    coords = probleme.node_coords
    tous = list(coords.keys())
    premier_sommet = tous[0]  # Le premier sommet ne peut pas être échangé

    for iteration in range(max_iter):
        amelioration = False
        for s in stations:
            # Ne jamais échanger le premier sommet (toujours une station)
            if s == premier_sommet:
                continue
            for c in tous:
                if c in stations:
                    continue
                # Tester de remplacer la station s par le client c
                nouvelles_stations = stations[:]
                nouvelles_stations.remove(s)
                nouvelles_stations.append(c)
                # S'assurer que le premier sommet est toujours présent
                if premier_sommet not in nouvelles_stations:
                    nouvelles_stations.insert(0, premier_sommet)
                    if len(nouvelles_stations) > p:
                        nouvelles_stations = nouvelles_stations[:p]

                # Reconstruire le cycle avec les nouvelles stations
                nouveau_cycle = tsp_plus_proche_voisin(matrice, nouvelles_stations, node_to_index)
                cout_new = cout_solution(
                    probleme, nouveau_cycle, nouvelles_stations, matrice, index_to_node, node_to_index
                )

                # Si amélioration, accepter le changement
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
    """
    Résolution exacte du problème Ring-Star par PLNE (Formulation Compacte).
    
    Variables (selon PDF page 6) :
    - z[i] = y_{ii} = 1 si le nœud i est une station, 0 sinon
    - y[i][j] = 1 si le client i est affecté à la station j, 0 sinon
    - x[i][j] = 1 si l'arête (i,j) est dans l'anneau, 0 sinon
    - f[i][j] = flot circulant sur l'arc (i,j) pour assurer la connexité (formulation par flots)
    
    Contraintes implémentées (PDF page 6) :
    - (1) Exactement p stations
    - (2) Chaque nœud affecté à exactement une station
    - (3) On ne peut affecter qu'à une station (y_{ij} ≤ y_{jj})
    - (4) Contraintes de degré pour l'anneau (2 arêtes par station)
    - (5) Les arcs de l'anneau ne peuvent exister qu'entre stations
    - (5)–(7) Contraintes de flot pour éliminer les sous-tours
    - (9) Inégalités de renforcement (ajoutées en dur)
    - CONTRAINTE FIXE : Le sommet 1 est toujours une station
    
    Objectif : Minimiser coût(anneau) + coût(affectations)
    """
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    noeuds = list(index_to_node.values())
    n = len(noeuds)

    # Créer le modèle PLNE
    model = pulp.LpProblem("RingStar", pulp.LpMinimize)

    # ===== VARIABLES DE DÉCISION =====
    # x[i][j] = 1 si l'arête (i->j) est dans l'anneau, 0 sinon
    x = pulp.LpVariable.dicts("x", (noeuds, noeuds), 0, 1, cat="Binary")
    
    # z[i] = 1 si le nœud i est une station, 0 sinon
    z = pulp.LpVariable.dicts("z", noeuds, 0, 1, cat="Binary")
    
    # y[i][j] = 1 si le client i est affecté à la station j, 0 sinon
    y = pulp.LpVariable.dicts("y", (noeuds, noeuds), 0, 1, cat="Binary")
    
    # f[i][j] : variables de flot pour assurer la connexité (formulation par flots)
    # Bornées entre 0 et p-1 comme dans la formulation compacte
    f = pulp.LpVariable.dicts("f", (noeuds, noeuds), lowBound=0, upBound=p - 1, cat="Continuous")

    # ===== FONCTION OBJECTIF =====
    # Minimiser : coût de l'anneau + coût des étoiles
    cout_anneau = pulp.lpSum(
        matrice[node_to_index[i]][node_to_index[j]] * x[i][j] 
        for i in noeuds for j in noeuds if i != j
    )
    cout_etoiles = pulp.lpSum(
        matrice[node_to_index[i]][node_to_index[j]] * y[i][j] 
        for i in noeuds for j in noeuds
    )
    model += cout_anneau + cout_etoiles

    # ===== CONTRAINTES =====
    
    # (1) Exactement p stations
    model += pulp.lpSum(z[i] for i in noeuds) == p

    # CONTRAINTE FIXE : Le sommet 1 (premier sommet) est TOUJOURS une station
    premier_sommet = noeuds[0]
    model += z[premier_sommet] == 1
    # Le premier sommet ne peut pas être affecté à une autre station
    for j in noeuds:
        if j != premier_sommet:
            model += y[premier_sommet][j] == 0

    # (2) Chaque nœud est affecté à exactement une station
    for i in noeuds:
        model += pulp.lpSum(y[i][j] for j in noeuds) == 1

    # (3) On ne peut affecter un client qu'à une station (z[j] = 1)
    for i in noeuds:
        for j in noeuds:
            model += y[i][j] <= z[j]

    # Lier explicitement z[i] et y[i][i] comme dans la formulation du p-médian :
    # z[i] = y_{ii} pour tout i
    for i in noeuds:
        model += z[i] == y[i][i]

    # (4) Contraintes de degré pour l'anneau (PDF page 6) :
    #     ∑_{ij∈δ(i)} x_{ij} = 2y_{ii} ∀i ∈ V
    #     Chaque station a exactement 2 arêtes incidentes (une entrante, une sortante)
    #     Les non-stations n'ont aucune arête dans l'anneau
    for i in noeuds:
        # Degré sortant = 1 si station, 0 sinon
        model += pulp.lpSum(x[i][j] for j in noeuds if i != j) == z[i]
        # Degré entrant = 1 si station, 0 sinon  
        model += pulp.lpSum(x[j][i] for j in noeuds if i != j) == z[i]
        # Total = 2*z[i] = 2 arêtes si station (conforme à la contrainte (4) du PDF)

    # (5) Les arcs de l'anneau ne peuvent exister qu'entre stations
    for i in noeuds:
        for j in noeuds:
            if i == j:
                model += x[i][j] == 0  # Pas de boucle
            else:
                model += x[i][j] <= z[i]  # i doit être station
                model += x[i][j] <= z[j]  # j doit être station

    # (9) Inégalités de renforcement (ajoutées en dur comme recommandé)
    # yjj >= xij pour tout i != 1, j
    for i in noeuds:
        if i != premier_sommet:
            for j in noeuds:
                model += z[j] >= x[i][j]

    # (5)–(7) Contraintes de flot pour éliminer les sous-tours (formulation compacte par flots)
    # (5) Le sommet 1 envoie un flot total de valeur p-1
    model += pulp.lpSum(f[premier_sommet][j] for j in noeuds if j != premier_sommet) == p - 1

    # (6) Conservation du flot et décrémentation aux stations :
    #     ∑_{j≠i} z_{ji} = ∑_{j≠1,i} z_{ij} + y_{ii}  pour tout i ≠ 1
    for i in noeuds:
        if i == premier_sommet:
            continue
        flux_entrant = pulp.lpSum(f[j][i] for j in noeuds if j != i)
        flux_sortant = pulp.lpSum(f[i][j] for j in noeuds if j != premier_sommet and j != i)
        model += flux_entrant == flux_sortant + y[i][i]

    # (7) Capacité du flot sur les arcs :
    #     z_{ij} + z_{ji} ≤ (p − 1) x_{ij}  pour tout i ∈ V, j ∈ V \ {1, i}
    for i in noeuds:
        for j in noeuds:
            if j == premier_sommet or j == i:
                continue
            model += f[i][j] + f[j][i] <= (p - 1) * x[i][j]

    # ===== RÉSOLUTION =====
    model.solve(pulp.PULP_CBC_CMD(msg=False))

    # ===== EXTRACTION DE LA SOLUTION =====
    status = model.status
    if status != pulp.LpStatusOptimal:
        print(f"⚠️  Le solveur n'a pas trouvé de solution optimale. Statut : {pulp.LpStatus[status]}")
        print("   Utilisation d'une solution heuristique à la place...")
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations

    # Extraire les stations
    stations = [i for i in noeuds if pulp.value(z[i]) is not None and pulp.value(z[i]) > 0.5]

    # Vérifier que le premier sommet est bien une station
    premier_sommet = noeuds[0]
    if premier_sommet not in stations:
        stations.insert(0, premier_sommet)
        if len(stations) > p:
            # Retirer une station si on en a trop
            stations = [premier_sommet] + [s for s in stations[1:] if s != premier_sommet][:p-1]

    if not stations or len(stations) != p:
        print(f"⚠️  Problème avec les stations trouvées ({len(stations)} au lieu de {p})")
        print("   Utilisation d'une solution heuristique à la place...")
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations

    # Extraire les arcs de l'anneau
    edges_metro = []
    for i in noeuds:
        for j in noeuds:
            if i != j and pulp.value(x[i][j]) is not None and pulp.value(x[i][j]) > 0.5:
                edges_metro.append((i, j))

    # Reconstruire le cycle à partir des arcs
    cycle = reconstruire_cycle_depuis_arcs(edges_metro, stations)
    
    if not cycle or len(cycle) != p:
        print(f"⚠️  Problème avec le cycle reconstruit ({len(cycle) if cycle else 0} stations au lieu de {p})")
        print("   Utilisation d'une solution heuristique à la place...")
        cycle, stations = heuristique_rapide(probleme, p)
        return cycle, stations
    
    return cycle, stations


# Petit main de test
def main():
    fichier = "data/ulysses16.tsp"

    probleme = chargerInstance(fichier)
    
    # Calcul automatique du nombre de stations
    p = calculerNombreStations(probleme)
    print(f"Nombre de nœuds : {len(probleme.node_coords)}, K = {p} (calculé automatiquement)")

    # Heuristique rapide
    cycle_h, stations_h = heuristique_rapide(probleme, p)
    afficherSolution(probleme, cycle_h, stations_h, methode="heuristique")

    # Amélioration locale
    cycle_c, stations_c, cout_c = amelioration_locale(probleme, p, cycle_h, stations_h)
    afficherSolution(probleme, cycle_c, stations_c, methode="amelioration_locale")

    # Méthode exacte (attention plus lente)
    cycle_d, stations_d = methode_exacte(probleme, p)
    afficherSolution(probleme, cycle_d, stations_d, methode="exact")


if __name__ == "__main__":
    main()

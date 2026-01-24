from base import *

def choisirStations_aleatoire(probleme, p):
    noeuds = list(probleme.node_coords.keys())
    pSommet = noeuds[0]
    autreNoeuds = [n for n in noeuds if n != pSommet]
    autresStations = random.sample(autreNoeuds, min(p - 1, len(autreNoeuds)))
    return [pSommet] + autresStations

def plusProcheVoisin(matrice, stations, noeudIndex):

    if not stations:
        return []

    pSommet = stations[0]
    nonVisites = set(stations)
    courant = pSommet
    cycle = [courant]
    nonVisites.remove(courant)

    while nonVisites:
        i = noeudIndex[courant]
        meilleur = None
        bestDist = float("inf")
        for s in nonVisites:
            j = noeudIndex[s]
            d = matrice[i][j]
            if d < bestDist:
                bestDist = d
                meilleur = s
        cycle.append(meilleur)
        nonVisites.remove(meilleur)
        courant = meilleur

    return cycle

def heuristiqueRapide(probleme, p):
    matrice, indexNoeud, noeudIndex = obtenirMatriceDistances(probleme)
    stations = choisirStations_aleatoire(probleme, p)
    cycle = plusProcheVoisin(matrice, stations, noeudIndex)
    return cycle, stations

def main():
    pass

if __name__ == "__main__":
    main()
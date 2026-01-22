import sys
import time

from instance import (
    chargerInstance,
    heuristique_rapide,
    afficherSolution,
    obtenirMatriceDistances,
    cout_solution,
)


def main():
    if len(sys.argv) < 3:
        print("Usage : python heuristique.py <fichier.tsp> <K>")
        sys.exit(1)

    fichier = sys.argv[1]
    try:
        p = int(sys.argv[2])
    except ValueError:
        print("K doit être un entier.")
        sys.exit(1)

    # Les fichiers .tsp sont dans le dossier data/
    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Heuristique rapide ===")
    print(f"Fichier : {fichier}, K = {p}")
    
    debut = time.time()
    cycle, stations = heuristique_rapide(probleme, p)
    temps = time.time() - debut

    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cout = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)

    print(f"Coût de la solution : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations)


if __name__ == "__main__":
    main()


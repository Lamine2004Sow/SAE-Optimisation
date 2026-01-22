import sys
import time

from instance import (
    chargerInstance,
    methode_exacte,
    afficherSolution,
    obtenirMatriceDistances,
    cout_solution,
)


def main():
    if len(sys.argv) < 3:
        print("Usage : python exactPlne.py <fichier.tsp> <K>")
        sys.exit(1)

    fichier = sys.argv[1]
    try:
        p = int(sys.argv[2])
    except ValueError:
        print("K doit être un entier.")
        sys.exit(1)

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Méthode exacte (PLNE) ===")
    print(f"Fichier : {fichier}, K = {p}")
    print("Résolution en cours... (peut prendre du temps)")
    
    debut = time.time()
    cycle, stations = methode_exacte(probleme, p)
    temps = time.time() - debut

    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cout = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)

    print(f"Coût de la solution optimale : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations)


if __name__ == "__main__":
    main()


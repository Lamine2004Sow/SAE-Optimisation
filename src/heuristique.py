import sys
import time

from instance import (
    chargerInstance,
    calculerNombreStations,
    heuristique_rapide,
    cout_solution,
    obtenirMatriceDistances,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python heuristique.py <fichier.tsp> [p]")
        sys.exit(1)

    fichier = sys.argv[1]

    # Les fichiers .tsp sont dans le dossier data/
    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    # Récupérer p en argument ou utiliser la valeur par défaut
    if len(sys.argv) == 3:
        p = int(sys.argv[2])
    else:
        p = calculerNombreStations(probleme)

    print(f"=== Heuristique rapide pour Ring-Star ===")
    print(f"Fichier : {fichier}")
    print(f"Nombre de nœuds : {len(probleme.node_coords)}")
    print(f"Nombre de stations fixé : {p}")
    
    debut = time.time()
    cycle, stations = heuristique_rapide(probleme, p)
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cout = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Coût de la solution : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="heuristique")


if __name__ == "__main__":
    main()


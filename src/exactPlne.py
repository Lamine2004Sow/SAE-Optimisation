import sys
import time

from instance import (
    chargerInstance,
    calculerNombreStations,
    methode_exacte,
    cout_solution,
    obtenirMatriceDistances,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python exactPlne.py <fichier.tsp> [p]")
        sys.exit(1)

    fichier = sys.argv[1]

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    # Récupérer p en argument ou utiliser la valeur par défaut
    if len(sys.argv) == 3:
        p = int(sys.argv[2])
    else:
        p = calculerNombreStations(probleme)

    print(f"=== Résolution exacte du problème Ring-Star (PLNE) ===")
    print(f"Fichier : {fichier}")
    print(f"Nombre de nœuds : {len(probleme.node_coords)}")
    print(f"Nombre de stations fixé : {p}")
    print("Résolution en cours... (peut prendre du temps pour les grandes instances)")
    
    debut = time.time()
    cycle, stations = methode_exacte(probleme, p)
    matrice, index_to_node, node_to_index = obtenirMatriceDistances(probleme)
    cout = cout_solution(probleme, cycle, stations, matrice, index_to_node, node_to_index)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Coût de la solution optimale : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="exact")


if __name__ == "__main__":
    main()


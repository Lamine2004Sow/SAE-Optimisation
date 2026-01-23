import sys
import time

from instance import (
    chargerInstance,
    heuristique_rapide_optimisee,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python heuristique.py <fichier.tsp>")
        sys.exit(1)

    fichier = sys.argv[1]

    # Les fichiers .tsp sont dans le dossier data/
    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Heuristique rapide pour Ring-Star ===")
    print(f"Fichier : {fichier}")
    print(f"Nombre de nœuds : {len(probleme.node_coords)}")
    
    debut = time.time()
    p_optimal, cycle, stations, cout = heuristique_rapide_optimisee(probleme)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Nombre optimal de stations : {p_optimal}")
    print(f"Coût de la solution : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="heuristique")


if __name__ == "__main__":
    main()


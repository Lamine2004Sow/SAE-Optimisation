import sys
import time

from instance import (
    chargerInstance,
    amelioration_locale_optimisee,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python metaheuristique.py <fichier.tsp>")
        sys.exit(1)

    fichier = sys.argv[1]

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Métaheuristique (amélioration locale avec optimisation du nombre de stations) ===")
    print(f"Fichier : {fichier}, Nombre de nœuds : {len(probleme.node_coords)}")
    
    debut = time.time()
    p_optimal, cycle, stations, cout = amelioration_locale_optimisee(probleme)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Nombre optimal de stations : {p_optimal}")
    print(f"Coût de la solution optimale : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="metaheuristique")


if __name__ == "__main__":
    main()

import sys
import time

from instance import (
    chargerInstance,
    methode_exacte_optimisee,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python exactPlne.py <fichier.tsp>")
        sys.exit(1)

    fichier = sys.argv[1]

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Méthode exacte (PLNE avec optimisation du nombre de stations) ===")
    print(f"Fichier : {fichier}, Nombre de nœuds : {len(probleme.node_coords)}")
    print("Résolution en cours... (peut prendre du temps)")
    
    debut = time.time()
    p_optimal, cycle, stations, cout = methode_exacte_optimisee(probleme)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Nombre optimal de stations : {p_optimal}")
    print(f"Coût de la solution optimale : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="exact")


if __name__ == "__main__":
    main()


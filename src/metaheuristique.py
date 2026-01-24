import sys
import time

from instance import (
    chargerInstance,
    calculerNombreStations,
    heuristique_rapide,
    amelioration_locale,
    afficherSolution,
)


def main():
    if len(sys.argv) < 2:
        print("Usage : python metaheuristique.py <fichier.tsp> [p]")
        sys.exit(1)

    fichier = sys.argv[1]

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    # Récupérer p en argument ou utiliser la valeur par défaut
    if len(sys.argv) == 3:
        p = int(sys.argv[2])
    else:
        p = calculerNombreStations(probleme)

    print(f"=== Amélioration locale pour Ring-Star ===")
    print(f"Fichier : {fichier}")
    print(f"Nombre de nœuds : {len(probleme.node_coords)}")
    print(f"Nombre de stations fixé : {p}")
    
    debut = time.time()
    # 1. Générer solution initiale
    cycle_init, stations_init = heuristique_rapide(probleme, p)
    # 2. Améliorer
    cycle, stations, cout = amelioration_locale(probleme, p, cycle_init, stations_init)
    temps = time.time() - debut

    print(f"\n=== Résultat ===")
    print(f"Coût de la solution optimale : {cout:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations}")
    
    afficherSolution(probleme, cycle, stations, methode="metaheuristique")


if __name__ == "__main__":
    main()

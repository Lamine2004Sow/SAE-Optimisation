import sys
import time

from instance import (
    chargerInstance,
    heuristique_rapide,
    amelioration_locale,
    afficherSolution,
)


def main():
    if len(sys.argv) < 3:
        print("Usage : python metaheuristique.py <fichier.tsp> <K>")
        sys.exit(1)

    fichier = sys.argv[1]
    try:
        p = int(sys.argv[2])
    except ValueError:
        print("K doit être un entier.")
        sys.exit(1)

    chemin = f"data/{fichier}"

    probleme = chargerInstance(chemin)

    print(f"=== Métaheuristique (amélioration locale) ===")
    print(f"Fichier : {fichier}, K = {p}")
    
    # On part de l'heuristique rapide
    print("Étape 1 : Heuristique rapide...")
    cycle_h, stations_h = heuristique_rapide(probleme, p)

    # Puis on améliore avec la métaheuristique locale
    print("Étape 2 : Amélioration locale...")
    debut = time.time()
    cycle_m, stations_m, cout_m = amelioration_locale(probleme, p, cycle_h, stations_h)
    temps = time.time() - debut

    print(f"Coût de la solution optimale : {cout_m:.2f}")
    print(f"Temps de résolution : {temps:.4f} secondes")
    print(f"Stations : {stations_m}")
    
    afficherSolution(probleme, cycle_m, stations_m)


if __name__ == "__main__":
    main()

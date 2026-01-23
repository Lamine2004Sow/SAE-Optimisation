"""
Script simple pour visualiser le nuage de points d'une instance TSP.
Utile pour voir les données avant de résoudre le problème.
"""
import sys
from instance import chargerInstance, afficherNuagePoints


def main():
    if len(sys.argv) < 2:
        print("Usage : python visualisation.py <fichier.tsp>")
        print("Exemple : python visualisation.py ulysses16.tsp")
        sys.exit(1)

    fichier = sys.argv[1]
    chemin = f"data/{fichier}"

    print(f"=== Visualisation du nuage de points ===")
    print(f"Fichier : {fichier}")
    
    probleme = chargerInstance(chemin)
    print(f"Nombre de nœuds : {len(probleme.node_coords)}")
    
    afficherNuagePoints(probleme)
    print("Visualisation terminée.")


if __name__ == "__main__":
    main()

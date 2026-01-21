# SAE-Optimisation Project

Ce projet implémente différentes méthodes de résolution pour le problème du voyageur de commerce (TSP - Traveling Salesman Problem). Il propose trois approches :

- **Méthode exacte** : Résolution par programmation linéaire en nombres entiers (PLNE)
- **Heuristique** : Méthode rapide pour obtenir une solution approchée
- **Métaheuristique** : Algorithme d'optimisation avancé pour améliorer les solutions

Le projet utilise des instances de test issues de la bibliothèque TSPLIB95.

## Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez le dépôt ou téléchargez le projet
2. Installez les dépendances en utilisant le makefile :

```bash
make install
```

Cette commande crée un environnement virtuel Python (`.venv`) et installe toutes les dépendances nécessaires listées dans `requirements.txt`.

## Structure du projet

```text
SAE-Optimisation/
├── data/              # Instances TSP (fichiers .tsp)
├── src/               # Code source Python
│   ├── instance.py    # Chargement et manipulation des instances TSP
│   ├── exactPlne.py   # Résolution exacte par PLNE
│   ├── heuristique.py # Méthode heuristique
│   └── metaheuristique.py # Méthode métaheuristique
├── makefile           # Automatisation des commandes
├── requirements.txt   # Dépendances Python
└── README.md          # Ce fichier
```

## Utilisation

### Commandes disponibles

Le projet utilise un makefile pour simplifier l'exécution. Voici les commandes disponibles :

#### Afficher l'aide

```bash
make help
```

#### Lancer la méthode exacte (PLNE)

```bash
make run-exact
```

Par défaut, exécute `exactPlne.py` sur l'instance `ulysses16.tsp` avec le paramètre `5`.

#### Lancer l'heuristique

```bash
make run-heuristique
```

Par défaut, exécute `heuristique.py` sur l'instance `st70.tsp` avec le paramètre `10`.

#### Lancer la métaheuristique

```bash
make run-meta
```

Par défaut, exécute `metaheuristique.py` sur l'instance `st70.tsp` avec le paramètre `10`.

#### Lancer la visualisation

```bash
make run-visualisation
```

Par défaut, exécute `visualisation.py` sur l'instance `ulysses16.tsp` avec le paramètre `5`.

#### Nettoyer les fichiers temporaires

```bash
make clean
```

Supprime les fichiers `__pycache__`, les fichiers `.pyc` et l'environnement virtuel.

### Exécution manuelle

Vous pouvez également exécuter les scripts Python directement :

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Exécuter un script
python src/exactPlne.py data/ulysses16.tsp 5
python src/heuristique.py data/st70.tsp 10
python src/metaheuristique.py data/st70.tsp 10
```

## Dépendances

Les dépendances principales sont :

- `matplotlib` : Visualisation des graphes
- `pulp` : Résolution de problèmes d'optimisation linéaire
- `numpy` : Calculs numériques
- `networkx` : Manipulation de graphes
- `tsplib95` : Chargement des instances TSP
- `pandas` : Manipulation de données

Toutes les dépendances sont listées dans `requirements.txt` et installées automatiquement lors de `make install`.

## Instances TSP

Le dossier `data/` contient de nombreuses instances TSP de différentes tailles, de `burma14.tsp` (14 villes) à `pla85900.tsp` (85900 villes). Les solutions optimales connues sont disponibles dans le fichier `data/solutions`.

## Notes

- Les instances TSP sont au format TSPLIB95
- Les méthodes exactes peuvent être très lentes pour les grandes instances
- Les heuristiques et métaheuristiques sont recommandées pour les instances de grande taille
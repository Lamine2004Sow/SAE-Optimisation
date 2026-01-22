# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PYTHON_SRC = ../$(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

# Commandes par défaut (Aide)
.PHONY: help install clean run-heuristique run-meta run-exact run-visualize

help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install          : Crée le venv et installe les dépendances"
	@echo "  make run-heuristique  : Lance l'heuristique"
	@echo "  make run-meta         : Lance la métaheuristique"
	@echo "  make run-exact        : Lance la méthode exacte"
	@echo "  make run-visualize    : Lance la visualisation"
	@echo "  make clean            : Nettoie les fichiers temporaires"

# Installation : Crée le venv sans pip, puis installe pip et les dépendances
install:
	@echo "--- Création de l'environnement virtuel (Mode manuel) ---"
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV) --without-pip
	@echo "--- Installation de pip à l'intérieur du venv ---"
	# On utilise curl pour injecter pip dans le venv
	curl -sS https://bootstrap.pypa.io/get-pip.py | $(PYTHON)
	@echo "--- Installation des dépendances ---"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "--- Installation terminée ! ---"

# Visualisation : Crée le fichier de visualisation du Graphe et de l'Itinéraire
run-visualisation:
	cd src && $(PYTHON_SRC) visualisation.py ../data/ulysses16.tsp 4
# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f *.pyc

# --- Exécution (Utilise le python du venv) ---

run-heuristique:
	cd src && $(PYTHON_SRC) heuristique.py ../data/ulysses16.tsp 4

run-meta:
	cd src && $(PYTHON_SRC) metaheuristique.py ../data/ulysses16.tsp 5

run-exact:
	cd src && $(PYTHON_SRC) exactPlne.py ../data/ulysses16.tsp 5 300

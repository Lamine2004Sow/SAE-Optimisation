# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

FILE ?= ulysses16.tsp
K ?= 6 # Nombre de stations

.PHONY: help install clean run-heuristique run-meta run-exact run-visualisation

# Commande d'aide
help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install                     : Crée le venv et installe les dépendances"
	@echo "  make run-heuristique FILE=... K=... : Lance l'heuristique"
	@echo "  make run-meta FILE=... K=...        : Lance la métaheuristique"
	@echo "  make run-exact FILE=... K=...       : Lance la méthode exacte"
	@echo "  make run-visualisation FILE=... K=... : Lance la visualisation"
	@echo "  make clean                       : Nettoie les fichiers temporaires"

# Installation
install:
	@echo "--- Création de l'environnement virtuel (Mode manuel) ---"
	rm -rf $(VENV)
	$(SYSTEM_PYTHON) -m venv $(VENV) --without-pip
	@echo "--- Installation de pip à l'intérieur du venv ---"
	curl -sS https://bootstrap.pypa.io/get-pip.py | $(PYTHON)
	@echo "--- Installation des dépendances ---"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "--- Installation terminée ! ---"

# --- Exécutions ---

run-heuristique:
	$(PYTHON) src/heuristique.py $(FILE) $(K)

run-meta:
	$(PYTHON) src/metaheuristique.py $(FILE) $(K)

run-exact:
	$(PYTHON) src/exactPlne.py $(FILE) $(K)

run-visualisation:
	$(PYTHON) src/visualisation.py $(FILE) $(K)

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f *.pyc

# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

FILE ?= ulysses16.tsp

.PHONY: help install clean run-heuristique run-meta run-exact run-visualisation

# Commande d'aide
help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install                     : Crée le venv et installe les dépendances"
	@echo "  make run-heuristique FILE=...    : Lance l'heuristique (K calculé automatiquement)"
	@echo "  make run-meta FILE=...            : Lance la métaheuristique (K calculé automatiquement)"
	@echo "  make run-exact FILE=...           : Lance la méthode exacte (K calculé automatiquement)"
	@echo "  make run-visualisation FILE=...   : Lance la visualisation (K calculé automatiquement)"
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
	$(PYTHON) src/heuristique.py $(FILE)

run-meta:
	$(PYTHON) src/metaheuristique.py $(FILE)

run-exact:
	$(PYTHON) src/exactPlne.py $(FILE)

run-visualisation:
	$(PYTHON) src/visualisation.py $(FILE)

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f *.pyc

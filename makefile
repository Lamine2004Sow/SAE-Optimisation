# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

# Commandes par défaut (Aide)
.PHONY: help install install-sys clean run-heuristique run-meta run-exact

help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install          : Crée le venv et installe les dépendances"
	@echo "  make install-sys      : Installe GLPK (sudo requis)"
	@echo "  make run-heuristique  : Lance l'heuristique"
	@echo "  make run-meta         : Lance la métaheuristique"
	@echo "  make run-exact        : Lance la méthode exacte"
	@echo "  make clean            : Nettoie les fichiers temporaires"

# Installation : Crée le venv et installe les libs DEDANS
install:
	$(SYSTEM_PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Installation GLPK (Système)
install-sys:
	sudo apt-get update && sudo apt-get install -y glpk-utils

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f *.pyc

# --- Exécution (Utilise le python du venv) ---

run-heuristique:
	$(PYTHON) heuristique.py st70.tsp 10

run-meta:
	$(PYTHON) metaheuristique.py st70.tsp 10

run-exact:
	$(PYTHON) exactPlne.py ulysses16.tsp 5
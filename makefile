# Variables
VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
SYSTEM_PYTHON = python3

FILE ?= ulysses16.tsp
P ?=

.PHONY: help install clean run-heuristique run-meta run-exact run-visualisation

# Commande d'aide
help:
	@echo "--- Makefile SAÉ Optimisation (Mode Venv) ---"
	@echo "Commandes disponibles :"
	@echo "  make install                     : Crée le venv et installe les dépendances"
	@echo "  make run-heuristique FILE=... [P=...] : Lance l'heuristique (p calculé automatiquement si non fourni)"
	@echo "  make run-meta FILE=... [P=...]     : Lance la métaheuristique (p calculé automatiquement si non fourni)"
	@echo "  make run-exact FILE=... [P=...]    : Lance la méthode exacte (p calculé automatiquement si non fourni)"
	@echo "  make run-visualisation FILE=...    : Lance la visualisation"
	@echo "  make clean                       : Nettoie les fichiers temporaires"
	@echo ""
	@echo "Exemples :"
	@echo "  make run-heuristique FILE=ulysses16.tsp"
	@echo "  make run-heuristique FILE=ulysses16.tsp P=5"

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
	@if [ -z "$(P)" ]; then \
		$(PYTHON) src/heuristique.py $(FILE); \
	else \
		$(PYTHON) src/heuristique.py $(FILE) $(P); \
	fi

run-meta:
	@if [ -z "$(P)" ]; then \
		$(PYTHON) src/metaheuristique.py $(FILE); \
	else \
		$(PYTHON) src/metaheuristique.py $(FILE) $(P); \
	fi

run-exact:
	@if [ -z "$(P)" ]; then \
		$(PYTHON) src/exactPlne.py $(FILE); \
	else \
		$(PYTHON) src/exactPlne.py $(FILE) $(P); \
	fi

run-visualisation:
	$(PYTHON) src/visualisation.py $(FILE)

# Nettoyage
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -f *.pyc

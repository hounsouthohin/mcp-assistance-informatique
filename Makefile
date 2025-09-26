# Makefile pour le serveur MCP d'assistance informatique

.PHONY: help build run stop clean logs test install dev

# Variables
IMAGE_NAME := mcp-it-assistant
CONTAINER_NAME := mcp-it-assistant
COMPOSE_FILE := docker-compose.yml
CONFIG_FILE := examples/mcp-config.json

# Couleurs pour les messages
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Aide par défaut
help: ## Affiche cette aide
	@echo "$(BLUE)🔧 Serveur MCP d'Assistance Informatique$(NC)"
	@echo ""
	@echo "$(YELLOW)Commandes disponibles:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Construction
build: ## Construit l'image Docker
	@echo "$(BLUE)🏗️  Construction de l'image Docker...$(NC)"
	docker build -t $(IMAGE_NAME) .
	@echo "$(GREEN)✅ Image construite avec succès$(NC)"

build-no-cache: ## Construit l'image Docker sans cache
	@echo "$(BLUE)🏗️  Construction de l'image Docker (sans cache)...$(NC)"
	docker build --no-cache -t $(IMAGE_NAME) .
	@echo "$(GREEN)✅ Image construite avec succès$(NC)"

# Démarrage et arrêt
up: ## Démarre les services avec Docker Compose
	@echo "$(BLUE)🚀 Démarrage des services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "$(GREEN)✅ Services démarrés$(NC)"

down: ## Arrête les services
	@echo "$(BLUE)🛑 Arrêt des services...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down
	@echo "$(GREEN)✅ Services arrêtés$(NC)"

restart: down up ## Redémarre les services

# Développement
dev: ## Démarre en mode développement (avec logs)
	@echo "$(BLUE)🛠️  Mode développement...$(NC)"
	docker-compose -f $(COMPOSE_FILE) up --build

run-local: ## Exécute le serveur localement (nécessite Python)
	@echo "$(BLUE)🐍 Exécution locale...$(NC)"
	python server.py

# Monitoring et logs
logs: ## Affiche les logs en temps réel
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-tail: ## Affiche les derniers logs
	docker-compose -f $(COMPOSE_FILE) logs --tail=100

status: ## Affiche le statut des services
	@echo "$(BLUE)📊 Statut des services:$(NC)"
	docker-compose -f $(COMPOSE_FILE) ps

stats: ## Affiche les statistiques des conteneurs
	@echo "$(BLUE)📈 Statistiques des conteneurs:$(NC)"
	docker stats --no-stream

# Tests et validation
test: ## Exécute les tests
	@echo "$(BLUE)🧪 Exécution des tests...$(NC)"
	docker-compose -f $(COMPOSE_FILE) exec $(CONTAINER_NAME) python -c "import psutil; print(f'Test CPU: {psutil.cpu_percent()}%')"
	@echo "$(GREEN)✅ Tests terminés$(NC)"

health: ## Vérifie la santé du conteneur
	@echo "$(BLUE)🏥 Vérification de santé...$(NC)"
	docker inspect --format='{{.State.Health.Status}}' $(CONTAINER_NAME) || echo "Pas de healthcheck configuré"

validate-config: ## Valide la configuration Docker Compose
	@echo "$(BLUE)✅ Validation de la configuration...$(NC)"
	docker-compose -f $(COMPOSE_FILE) config

# Installation et configuration
install: build ## Installation complète (build + up)
	@echo "$(BLUE)📦 Installation du serveur MCP...$(NC)"
	$(MAKE) up
	@echo "$(GREEN)🎉 Installation terminée!$(NC)"
	@echo ""
	@echo "$(YELLOW)Configuration Claude Desktop:$(NC)"
	@echo "Copiez le contenu de $(CONFIG_FILE) dans votre configuration mcp-toolkit-gateway"

install-deps: ## Installe les dépendances Python localement
	@echo "$(BLUE)📦 Installation des dépendances...$(NC)"
	pip install -r requirements.txt
	@echo "$(GREEN)✅ Dépendances installées$(NC)"

# Nettoyage
clean: ## Nettoie les ressources Docker
	@echo "$(BLUE)🧹 Nettoyage...$(NC)"
	docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans
	docker image rm $(IMAGE_NAME) 2>/dev/null || true
	docker system prune -f
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

clean-all: clean ## Nettoyage complet (images, volumes, réseaux)
	@echo "$(BLUE)🧹 Nettoyage complet...$(NC)"
	docker system prune -a -f
	@echo "$(GREEN)✅ Nettoyage complet terminé$(NC)"

# Utilitaires
shell: ## Ouvre un shell dans le conteneur
	docker-compose -f $(COMPOSE_FILE) exec $(CONTAINER_NAME) /bin/bash

exec: ## Exécute une commande dans le conteneur (usage: make exec CMD="commande")
	docker-compose -f $(COMPOSE_FILE) exec $(CONTAINER_NAME) $(CMD)

backup: ## Crée une sauvegarde des données
	@echo "$(BLUE)💾 Création de la sauvegarde...$(NC)"
	mkdir -p backups
	tar -czf backups/mcp-backup-$(shell date +%Y%m%d-%H%M%S).tar.gz data logs
	@echo "$(GREEN)✅ Sauvegarde créée$(NC)"

# Documentation
docs: ## Génère la documentation
	@echo "$(BLUE)📚 Génération de la documentation...$(NC)"
	@echo "Configuration exemple pour Claude Desktop:"
	@cat $(CONFIG_FILE)

# Commandes de développement avancées
lint: ## Vérifie le code Python
	@echo "$(BLUE)🔍 Vérification du code...$(NC)"
	python -m flake8 server.py || echo "Installer flake8: pip install flake8"

format: ## Formate le code Python
	@echo "$(BLUE)🎨 Formatage du code...$(NC)"
	python -m black server.py || echo "Installer black: pip install black"

security-scan: ## Scan de sécurité des dépendances
	@echo "$(BLUE)🔒 Scan de sécurité...$(NC)"
	python -m safety check || echo "Installer safety: pip install safety"

# Informations
version: ## Affiche les versions des composants
	@echo "$(BLUE)📋 Versions des composants:$(NC)"
	@echo "Docker: $(shell docker --version)"
	@echo "Docker Compose: $(shell docker-compose --version)"
	@echo "Python: $(shell python --version 2>&1)"

info: ## Affiche les informations du projet
	@echo "$(BLUE)ℹ️  Informations du projet:$(NC)"
	@echo "Nom: $(IMAGE_NAME)"
	@echo "Conteneur: $(CONTAINER_NAME)"
	@echo "Configuration: $(CONFIG_FILE)"
	@echo "Compose: $(COMPOSE_FILE)"
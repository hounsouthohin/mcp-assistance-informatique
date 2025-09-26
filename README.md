# 🔧 Serveur MCP d'Assistance Informatique

Un serveur **Model Context Protocol (MCP)** complet conçu pour l'assistance informatique et le support technique. Ce projet expose une collection d'outils système utiles via une API standardisée MCP.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Outils disponibles](#-outils-disponibles)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Configuration](#-configuration)
- [API HTTP](#-api-http)
- [Sécurité](#-sécurité)
- [Développement](#-développement)

## 🚀 Fonctionnalités

- ✅ **Serveur MCP** conforme au protocole standard
- 🌐 **Interface HTTP REST** pour une utilisation facile
- 🐳 **Containerisation Docker** complète
- 🛡️ **Sécurisé** avec utilisateur non-root et limitations
- 📊 **Monitoring** avec health checks
- 🔧 **12 outils système** intégrés
- 📝 **Logging** complet et configurable

## 🛠️ Outils disponibles

### 🌍 Réseau et Connectivité
- **`ping_host`** - Ping un hôte réseau avec statistiques détaillées
- **`port_scan`** - Scanner les ports ouverts d'un hôte
- **`dns_lookup`** - Résolution DNS directe et inverse
- **`network_interfaces`** - Lister toutes les interfaces réseau
- **`http_request`** - Exécuter des requêtes HTTP personnalisées

### 💻 Système et Performance
- **`system_info`** - Informations complètes du système (CPU, RAM, disque)
- **`disk_usage`** - Analyse de l'utilisation du disque par partition
- **`process_list`** - Lister et filtrer les processus en cours
- **`check_service`** - Vérifier le statut des services système

### 🔧 Utilitaires
- **`calculator`** - Calculatrice sécurisée pour expressions mathématiques
- **`read_file`** - Lecture sécurisée de fichiers texte
- **`web_search`** - Recherche web basique (DuckDuckGo)

## 📦 Installation

### Prérequis
- Docker et Docker Compose
- Python 3.11+ (pour développement local)

### 🐳 Installation avec Docker (Recommandée)

1. **Cloner le projet**
```bash
git clone <repository-url>
cd mcp-assistance-informatique
```

2. **Construire et démarrer avec Docker Compose**
```bash
# Démarrage simple
docker-compose up -d

# Ou avec base de données (optionnel)
docker-compose --profile with-db up -d
```

3. **Vérifier le fonctionnement**
```bash
curl http://localhost:8000/health
```

### 🐍 Installation locale (Développement)

1. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

2. **Démarrer le serveur MCP**
```bash
python mcp_server.py
```

3. **Ou démarrer le serveur HTTP**
```bash
python http_server.py
```

## 🎯 Utilisation

### Via Docker Compose

```bash
# Démarrer les services
docker-compose up -d

# Voir les logs
docker-compose logs -f mcp-server

# Arrêter les services
docker-compose down
```

### Requêtes MCP standard

```bash
# Lister les outils
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": "1"
  }'

# Appeler un outil
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "system_info",
      "arguments": {}
    },
    "id": "2"
  }'
```

### API REST simplifiée

```bash
# Informations système
curl http://localhost:8000/tools/system-info

# Ping un hôte
curl -X POST http://localhost:8000/tools/ping \
  -H "Content-Type: application/json" \
  -d '{"host": "google.com", "count": 4}'

# Scanner des ports
curl -X POST http://localhost:8000/tools/port-scan \
  -H "Content-Type: application/json" \
  -d '{"host": "localhost", "ports": "22,80,443"}'

# Calculatrice
curl -X POST http://localhost:8000/tools/calculator \
  -H "Content-Type: application/json" \
  -d '{"expression": "2 + 2 * 3"}'
```

## ⚙️ Configuration

### Variables d'environnement

```bash
# Niveau de logging
LOG_LEVEL=INFO

# Port du serveur HTTP
PORT=8000

# Mode debug
DEBUG=false
```

### Fichiers de configuration

- `docker-compose.yml` - Configuration des services
- `Dockerfile` - Configuration du container
- `requirements.txt` - Dépendances Python

### Volumes Docker

```yaml
volumes:
  - /var/log:/host/var/log:ro      # Logs système (lecture seule)
  - ./data:/app/data               # Données persistantes
  - ./config:/app/config:ro        # Configuration (lecture seule)
```

## 🌐 API HTTP

### Endpoints principaux

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Informations du serveur |
| `/health` | GET | Vérification de santé |
| `/tools` | GET | Liste des outils |
| `/mcp` | POST | Requêtes MCP standard |
| `/call/{tool_name}` | POST | Appel direct d'outil |

### Documentation interactive

Une fois le serveur démarré, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

## 🛡️ Sécurité

### Mesures de sécurité implémentées

- 🔒 **Utilisateur non-root** dans le container
- 📏 **Limitation des ressources** (CPU, mémoire)
- 🚫 **Validation des entrées** pour tous les outils
- 📂 **Accès fichiers limité** (taille max 10MB)
- 🌐 **Timeout réseau** configuré (10s max)
- 🔍 **Sanitisation** des expressions mathématiques

### Recommandations de déploiement

- Utiliser un reverse proxy (nginx, traefik)
- Configurer HTTPS avec certificats TLS
- Limiter l'accès réseau aux services nécessaires
- Surveiller les logs d'accès et d'erreur
- Effectuer des sauvegardes régulières

## 🔧 Développement

### Structure du projet

```
mcp-assistance-informatique/
├── mcp_server.py          # Serveur MCP principal
├── http_server.py         # Interface HTTP REST
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Orchestration Docker
├── README.md            # Documentation
├── data/               # Données persistantes
├── config/             # Fichiers de configuration
└── logs/               # Fichiers de logs
```

### Ajouter un nouvel outil

1. **Implémenter la méthode dans MCPServer**
```python
async def mon_nouvel_outil(self, param1: str, param2: int = 10) -> Dict[str, Any]:
    """Description de l'outil"""
    try:
        # Logique de l'outil
        result = {"param1": param1, "param2": param2}
        return result
    except Exception as e:
        return {"error": str(e)}
```

2. **Ajouter à la liste des outils**
```python
def __init__(self):
    self.tools = {
        # ... outils existants
        "mon_nouvel_outil": self.mon_nouvel_outil,
    }
```

3. **Définir le schéma dans list_tools_response**
```python
{
    "name": "mon_nouvel_outil",
    "description": "Description de l'outil",
    "inputSchema": {
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Description param1"},
            "param2": {"type": "integer", "description": "Description param2", "default": 10}
        },
        "required": ["param1"]
    }
}
```

### Tests

```bash
# Tests unitaires
python -m pytest tests/

# Test des endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/tools
```

### Logs

```bash
# Voir les logs en temps réel
docker-compose logs -f mcp-server

# Logs d'un service spécifique
docker logs mcp-assistance-informatique
```

## 📈 Monitoring

### Health checks

Le serveur inclut des vérifications de santé automatiques :
- Vérification HTTP toutes les 30 secondes
- Timeout de 10 secondes
- 3 tentatives avant échec

### Métriques disponibles

- Statut des services
- Utilisation des ressources
- Statistiques des appels d'outils
- Temps de réponse

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- 📧 Email : support@example.com
- 🐛 Issues : GitHub Issues
- 📖 Wiki : GitHub Wiki
- 💬 Discord : [Serveur Discord](https://discord.gg/example)

---

**Développé avec ❤️ pour l'assistance informatique**# mcp-assistance-informatique

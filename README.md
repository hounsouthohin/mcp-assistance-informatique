# 🔧 Serveur MCP d'Assistance Informatique

Un serveur **Model Context Protocol (MCP)** complet pour l'assistance informatique, exposant des outils essentiels pour le diagnostic, la maintenance et la surveillance système.

## 🚀 Fonctionnalités

### Outils Disponibles

| Outil | Description | Utilisation |
|-------|-------------|-------------|
| `search_web` | Recherche d'informations sur le web | Recherche de documentation, solutions |
| `calculator` | Calculatrice mathématique avancée | Calculs, fonctions trigonométriques |
| `system_info` | Informations système détaillées | CPU, mémoire, disque, réseau, processus |
| `ping_host` | Test de connectivité réseau | Diagnostic réseau, vérification d'accès |
| `read_file` | Lecture de fichiers texte | Consultation de logs, configurations |
| `http_request` | Requêtes HTTP personnalisées | Test d'APIs, vérification de services |
| `port_scan` | Scan de ports réseau | Audit de sécurité, diagnostic réseau |
| `log_analysis` | Analyse de fichiers de logs | Recherche d'erreurs, monitoring |

## 📋 Prérequis

- **Docker** et **Docker Compose**
- **Claude Desktop** avec mcp-toolkit-gateway configuré
- **Python 3.11+** (pour le développement local)

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd mcp-it-assistant
```

### 2. Construction avec Docker

```bash
# Construction de l'image
docker build -t mcp-it-assistant .

# Ou utiliser Docker Compose
docker-compose build
```

### 3. Déploiement avec Docker Compose

```bash
# Démarrage des services
docker-compose up -d

# Vérification du statut
docker-compose ps

# Consultation des logs
docker-compose logs -f mcp-it-assistant
```

## ⚙️ Configuration avec Claude Desktop

### Configuration mcp-toolkit-gateway

Pour utiliser ce serveur MCP avec Claude Desktop via mcp-toolkit-gateway, ajoutez cette configuration à votre fichier de configuration Claude Desktop :

```json
{
  "mcpServers": {
    "mcp-toolkit-gateway": {
      "command": "npx",
      "args": [
        "@anthropic-ai/mcp-toolkit-gateway",
        "--config-file",
        "/path/to/your/mcp-config.json"
      ]
    }
  }
}
```

### Fichier de configuration MCP (mcp-config.json)

```json
{
  "servers": {
    "it-assistant": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network=host",
        "-v", "/var/log:/host/var/log:ro",
        "-v", "./data:/app/data:rw",
        "mcp-it-assistant"
      ],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

### Configuration alternative (exécution locale)

Si vous préférez exécuter le serveur localement sans Docker :

```json
{
  "servers": {
    "it-assistant": {
      "command": "python",
      "args": ["/path/to/mcp-it-assistant/server.py"],
      "env": {
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

## 🚀 Utilisation

### Démarrage rapide

```bash
# Démarrage avec Docker Compose
docker-compose up -d

# Test de fonctionnement
docker-compose exec mcp-it-assistant python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%')"
```

### Exemples d'utilisation dans Claude Desktop

Une fois configuré, vous pouvez utiliser les outils directement dans Claude Desktop :

#### 1. Informations système
```
Peux-tu me donner les informations sur l'utilisation du CPU et de la mémoire ?
```

#### 2. Test de connectivité
```
Peux-tu pinger google.com pour vérifier la connectivité ?
```

#### 3. Analyse de logs
```
Peux-tu analyser le fichier /var/log/syslog à la recherche d'erreurs récentes ?
```

#### 4. Calculs techniques
```
Calcule la puissance nécessaire : sqrt(220^2 + 110^2) * 1.732
```

## 📁 Structure du projet

```
mcp-it-assistant/
├── server.py              # Serveur MCP principal
├── requirements.txt       # Dépendances Python
├── Dockerfile             # Configuration Docker
├── docker-compose.yml     # Orchestration Docker
├── README.md              # Documentation
├── nginx.conf             # Configuration proxy (optionnel)
├── logs/                  # Répertoire des logs
├── data/                  # Répertoire de données
└── examples/              # Exemples d'utilisation
    └── mcp-config.json    # Configuration exemple
```

## 🔧 Configuration avancée

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|---------|
| `MCP_TRANSPORT` | Type de transport MCP | `stdio` |
| `PYTHONUNBUFFERED` | Sortie Python non bufferisée | `1` |
| `TZ` | Fuseau horaire | `Europe/Paris` |

### Volumes Docker

- `./logs:/app/logs:ro` - Logs applicatifs (lecture seule)
- `./data:/app/data:rw` - Données persistantes (lecture/écriture)
- `/var/log:/host/var/log:ro` - Logs système hôte (lecture seule)

### Limites de ressources

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.25'
      memory: 128M
```

## 🔒 Sécurité

### Bonnes pratiques implémentées

1. **Utilisateur non-root** dans le conteneur
2. **Limitation des ressources** CPU/mémoire
3. **Accès en lecture seule** aux logs système
4. **Validation des entrées** pour tous les outils
5. **Timeout sur les opérations** réseau
6. **Sandboxing** des calculs mathématiques

### Recommandations

- Limiter l'accès réseau si non nécessaire
- Surveiller les logs d'utilisation
- Configurer un firewall approprié
- Utiliser des volumes chiffrés pour les données sensibles

## 🐛 Dépannage

### Problèmes courants

#### Le serveur ne démarre pas
```bash
# Vérifier les logs
docker-compose logs mcp-it-assistant

# Vérifier la configuration
docker-compose config
```

#### Erreurs de permissions
```bash
# Corriger les permissions des volumes
chmod -R 755 ./logs ./data
chown -R $USER:$USER ./logs ./data
```

#### Problèmes de connectivité réseau
```bash
# Tester la connectivité depuis le conteneur
docker-compose exec mcp-it-assistant ping google.com

# Vérifier la configuration réseau
docker network ls
docker network inspect mcp-it-assistant_mcp-network
```

### Logs et monitoring

```bash
# Logs en temps réel
docker-compose logs -f

# Logs spécifiques au service
docker-compose logs mcp-it-assistant

# Statistiques des conteneurs
docker stats
```

## 🔄 Mise à jour

```bash
# Arrêter les services
docker-compose down

# Mettre à jour le code
git pull

# Reconstruire et redémarrer
docker-compose build --no-cache
docker-compose up -d
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues GitHub** : Pour signaler des bugs ou demander des fonctionnalités
- **Discussions** : Pour les questions générales et l'aide communautaire
- **Wiki** : Pour la documentation détaillée

## 🔗 Liens utiles

- [Documentation MCP](https://modelcontextprotocol.io/)
- [Claude Desktop](https://claude.ai/desktop)
- [mcp-toolkit-gateway](https://github.com/anthropics/mcp-toolkit-gateway)
- [Docker Documentation](https://docs.docker.com/)

---

**Note** : Ce serveur MCP est conçu pour être utilisé avec Claude Desktop via mcp-toolkit-gateway. Assurez-vous d'avoir correctement configuré votre environnement avant utilisation.

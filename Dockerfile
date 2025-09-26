# Utilise une image Python légère
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="IT Assistant Team"
LABEL description="Serveur MCP pour assistance informatique"
LABEL version="1.0.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV MCP_TRANSPORT=stdio

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    ping \
    iputils-ping \
    net-tools \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY server.py .

# Changer la propriété des fichiers
RUN chown -R mcpuser:mcpuser /app

# Basculer vers l'utilisateur non-root
USER mcpuser

# Exposer le port (optionnel, pour futures extensions)
EXPOSE 8000

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import psutil; psutil.cpu_percent()" || exit 1

# Commande par défaut
CMD ["python", "server.py"]
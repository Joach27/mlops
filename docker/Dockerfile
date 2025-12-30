# docker/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'application
COPY api/ ./api/
COPY model/ ./model/

# Exposition du port
EXPOSE 5000

# Commande de démarrage
CMD ["python", "api/app.py"]
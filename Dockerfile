# Python runtime
FROM python:3.11-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Créer le répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements
COPY requirements.txt /app/

# Installer les dépendances Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
    
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY systeme_notification /app/

# Créer le répertoire pour les fichiers statiques
RUN mkdir -p /app/staticfiles

# Collecter les fichiers statiques
RUN python manage.py collectstatic --noinput --clear || true

# Créer un utilisateur non-root
RUN useradd -m -u 1000 django && \
    chown -R django:django /app

# Expose le port interne (optionnel, pour la doc)
EXPOSE 8000

# Commande de démarrage
CMD ["sh", "-c", "gunicorn systeme_notification.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3"]

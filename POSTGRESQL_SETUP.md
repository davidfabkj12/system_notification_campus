# 🐘 Configuration PostgreSQL - Guide Complet

## 📋 3 Façons de configurer PostgreSQL

### 1️⃣ Pour Docker (Le plus simple) ✅
### 2️⃣ Pour Railway/Render (Hébergement cloud)
### 3️⃣ Pour installation locale Windows/Linux

---

## 1️⃣ Configuration Docker (RECOMMANDÉ pour développement)

### Tout est déjà configuré! 🎉

PostgreSQL est déjà inclus dans `docker-compose.yml`. Il suffit de:

```bash
# 1. Créer le fichier .env
cp .env.example .env

# 2. Démarrer Docker (PostgreSQL inclus)
docker-compose up --build

# 3. C'est tout! PostgreSQL est prêt
```

**Configuration automatique:**
- Base de données: `notificationdb`
- Utilisateur: `notifuser`
- Mot de passe: `notifpass123`
- Host: `db` (dans Docker)
- Port: `5432`

**Pas besoin d'installer PostgreSQL sur votre machine!**

---

## 2️⃣ Configuration Cloud (Railway/Render)

### Railway (Le plus simple)

1. **Créer le projet sur Railway:**
   - Allez sur https://railway.app/
   - New Project → Deploy from GitHub repo

2. **Ajouter PostgreSQL:**
   - Cliquez sur **+ New**
   - Sélectionnez **Database** → **PostgreSQL**
   - Railway crée automatiquement la base de données

3. **Configurer les variables:**
   - Cliquez sur votre service web
   - Allez dans **Variables**
   - Ajoutez:
   ```
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   ```

4. **C'est tout!** Django se connecte automatiquement.

### Render

1. **Créer PostgreSQL:**
   - Dashboard Render → **New** → **PostgreSQL**
   - Name: `notificationdb`
   - Plan: **Free**

2. **Copier l'URL:**
   - Copiez **Internal Database URL**
   - Format: `postgresql://user:pass@host:5432/dbname`

3. **Configurer le Web Service:**
   - Dans votre Web Service
   - **Environment** → Add:
   ```
   DATABASE_URL = (collez l'URL PostgreSQL)
   ```

---

## 3️⃣ Installation Locale (Windows/Linux/Mac)

### Windows

#### Option A: Avec installateur officiel

1. **Télécharger PostgreSQL:**
   - https://www.postgresql.org/download/windows/
   - Version 15 ou 16 recommandée

2. **Installer:**
   - Exécutez l'installateur
   - Port: **5432** (par défaut)
   - Mot de passe: **notez-le bien!**
   - Locale: **French, France** ou **Default locale**

3. **Créer la base de données:**
   ```bash
   # Ouvrir PowerShell
   
   # Se connecter à PostgreSQL
   psql -U postgres
   
   # Créer la base de données
   CREATE DATABASE notificationdb;
   
   # Créer l'utilisateur
   CREATE USER notifuser WITH PASSWORD 'votremotdepasse';
   
   # Donner les droits
   GRANT ALL PRIVILEGES ON DATABASE notificationdb TO notifuser;
   
   # Quitter
   \q
   ```

4. **Configurer Django:**
   
   Créez/modifiez `.env`:
   ```env
   DATABASE_URL=postgresql://notifuser:votremotdepasse@localhost:5432/notificationdb
   ```

#### Option B: Avec Docker Desktop

C'est plus simple! Utilisez `docker-compose up` comme expliqué dans la section 1.

### Linux (Ubuntu/Debian)

```bash
# 1. Installer PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# 2. Démarrer le service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# 3. Se connecter
sudo -u postgres psql

# 4. Créer la base de données
CREATE DATABASE notificationdb;
CREATE USER notifuser WITH PASSWORD 'votremotdepasse';
GRANT ALL PRIVILEGES ON DATABASE notificationdb TO notifuser;
\q

# 5. Modifier .env
DATABASE_URL=postgresql://notifuser:votremotdepasse@localhost:5432/notificationdb
```

### macOS

```bash
# Avec Homebrew
brew install postgresql@15
brew services start postgresql@15

# Créer la base de données
createdb notificationdb

# Se connecter
psql notificationdb

# Créer l'utilisateur
CREATE USER notifuser WITH PASSWORD 'votremotdepasse';
GRANT ALL PRIVILEGES ON DATABASE notificationdb TO notifuser;
\q

# Configurer .env
DATABASE_URL=postgresql://notifuser:votremotdepasse@localhost:5432/notificationdb
```

---

## 🔧 Configuration Django (déjà fait!)

Le fichier `settings.py` est déjà configuré pour PostgreSQL:

```python
# settings.py (déjà modifié)

import dj_database_url

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Production: PostgreSQL
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Développement: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'notifsysdb.sqlite3',
        }
    }
```

**Ça signifie:**
- Si `DATABASE_URL` existe → utilise PostgreSQL
- Sinon → utilise SQLite (développement local)

---

## 📝 Configuration du fichier .env

Créez `.env` à la racine du projet:

```env
# Django
SECRET_KEY=votre-secret-key-tres-longue
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL - Choisir selon votre configuration

# Pour Docker (docker-compose)
DATABASE_URL=postgresql://notifuser:notifpass123@db:5432/notificationdb

# Pour installation locale
# DATABASE_URL=postgresql://notifuser:votremotdepasse@localhost:5432/notificationdb

# Pour Railway (automatique)
# DATABASE_URL=${{Postgres.DATABASE_URL}}

# Pour Render (collez l'URL)
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

---

## 🚀 Après configuration PostgreSQL

### 1. Installer les dépendances

```bash
pip install psycopg2-binary dj-database-url
```

Ou:

```bash
pip install -r requirements_clean.txt
```

### 2. Migrer la base de données

```bash
# Avec Docker
docker-compose exec web python manage.py migrate

# Sans Docker
cd systeme_notification
python manage.py migrate
```

### 3. Créer un superuser

```bash
# Avec Docker
docker-compose exec web python manage.py createsuperuser

# Sans Docker
python manage.py createsuperuser
```

### 4. Créer des données de test (optionnel)

```bash
# Avec Docker
docker-compose exec web python create_demo_data.py

# Sans Docker
python create_demo_data.py
```

---

## 🧪 Tester la connexion PostgreSQL

### Méthode 1: Via Django shell

```bash
# Avec Docker
docker-compose exec web python manage.py shell

# Sans Docker
python manage.py shell
```

Dans le shell Python:
```python
from django.db import connection
print(connection.vendor)  # Devrait afficher: postgresql
print(connection.settings_dict['NAME'])  # Nom de la DB
```

### Méthode 2: Via psql (ligne de commande PostgreSQL)

```bash
# Se connecter à PostgreSQL
psql -h localhost -U notifuser -d notificationdb

# Lister les tables
\dt

# Quitter
\q
```

---

## 🐛 Dépannage

### Erreur: "psycopg2 not installed"

```bash
pip install psycopg2-binary
```

### Erreur: "connection refused"

**Vérifier que PostgreSQL est démarré:**

```bash
# Windows
# Ouvrir Services → PostgreSQL doit être "Running"

# Linux
sudo systemctl status postgresql

# macOS
brew services list
```

### Erreur: "authentication failed"

**Vérifier les credentials dans .env:**
```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

### Erreur: "database does not exist"

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base
CREATE DATABASE notificationdb;
```

### Erreur: "fe_sendauth: no password supplied"

**Ajouter le mot de passe dans DATABASE_URL:**
```env
DATABASE_URL=postgresql://notifuser:MOTDEPASSE@localhost:5432/notificationdb
```

---

## 🔐 Sécurité

### En développement local:
- ✅ Mot de passe simple OK
- ✅ `.env` dans `.gitignore`
- ✅ SQLite acceptable

### En production:
- ✅ Mot de passe fort et complexe
- ✅ DATABASE_URL via variables d'environnement
- ✅ PostgreSQL obligatoire (pas SQLite)
- ✅ Connexions SSL activées

---

## 📊 Comparaison des options

| Méthode | Difficulté | Avantages | Inconvénients |
|---------|------------|-----------|---------------|
| **Docker** | ⭐ Facile | Rien à installer | Nécessite Docker |
| **Cloud** | ⭐ Facile | Gratuit, managé | Dépend d'internet |
| **Local** | ⭐⭐⭐ Moyen | Contrôle total | Installation manuelle |

**Recommandation:** Utilisez **Docker** pour le développement, **Railway/Render** pour la production.

---

## 🎯 Quick Start (le plus rapide)

### Pour développement local avec Docker:

```bash
# 1. Créer .env
cp .env.example .env

# 2. Démarrer (PostgreSQL inclus)
docker-compose up -d

# 3. Migrer
docker-compose exec web python manage.py migrate

# 4. Créer superuser
docker-compose exec web python manage.py createsuperuser

# ✅ TERMINÉ!
```

### Pour production sur Railway:

1. Push sur GitHub
2. Railway → New Project → GitHub repo
3. + New → PostgreSQL
4. Variables: `DATABASE_URL = ${{Postgres.DATABASE_URL}}`
5. ✅ TERMINÉ!

---

## 📚 Ressources

- PostgreSQL Official: https://www.postgresql.org/
- Django PostgreSQL: https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes
- psycopg2: https://www.psycopg.org/docs/
- Railway Docs: https://docs.railway.app/databases/postgresql
- Render Docs: https://render.com/docs/databases

---

## 💡 Conseils

1. **Pour débuter:** Utilisez Docker (aucune installation)
2. **Pour apprendre:** Installez PostgreSQL localement
3. **Pour production:** Utilisez Railway ou Render (gratuit et managé)
4. **Toujours:** Sauvegardez vos données en production
5. **Jamais:** Ne commitez pas les mots de passe

---

**Version:** 1.0  
**Status:** ✅ Prêt à l'emploi  
**Recommandation:** Docker pour dev, Railway pour prod

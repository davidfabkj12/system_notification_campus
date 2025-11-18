# 🐳 Docker + Hébergement Gratuit - Guide Complet

## 📋 Fichiers Docker créés

- ✅ `Dockerfile` - Image Docker pour l'application
- ✅ `docker-compose.yml` - Orchestration des services (Django, PostgreSQL, Redis, Nginx)
- ✅ `.env.example` - Template des variables d'environnement
- ✅ `nginx.conf` - Configuration Nginx pour reverse proxy
- ✅ `.dockerignore` - Fichiers à exclure de l'image Docker
- ✅ `requirements.txt` - Dépendances Python (mis à jour)
- ✅ `settings.py` - Configuration Django adaptée pour Docker

---

## 🚀 Utilisation en local avec Docker

### 1. Créer le fichier .env
```bash
cp .env.example .env
```

### 2. Construire et démarrer les conteneurs
```bash
docker-compose up --build
```

### 3. Créer un superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Accéder à l'application
- Application: http://localhost
- Dashboard: http://localhost/dashboard/
- Admin: http://localhost/admin/

---

## 🆓 Hébergement Gratuit - Options

### Option 1: Railway (Recommandé) ⭐

**Avantages:**
- 5$ de crédit gratuit/mois (suffisant pour votre app)
- PostgreSQL inclus
- Déploiement automatique depuis GitHub
- SSL gratuit
- Très simple

**Étapes:**

1. **Créer un compte sur Railway**
   - Allez sur https://railway.app/
   - Connectez-vous avec GitHub

2. **Créer le fichier railway.json**
   ```json
   {
     "$schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "DOCKERFILE",
       "dockerfilePath": "Dockerfile"
     },
     "deploy": {
       "startCommand": "python manage.py migrate && gunicorn systeme_notification.wsgi:application --bind 0.0.0.0:$PORT",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

3. **Créer un nouveau projet Railway**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

4. **Ajouter PostgreSQL**
   - Cliquez sur "+ New"
   - Sélectionnez "Database" → "PostgreSQL"

5. **Configurer les variables d'environnement**
   Dans l'onglet "Variables":
   ```
   SECRET_KEY=votre-secret-key-tres-long-et-securise
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   ```

6. **Déployer**
   - Railway déploie automatiquement
   - Votre app sera disponible sur: https://votre-app.railway.app

---

### Option 2: Render ⭐

**Avantages:**
- Gratuit pour toujours (avec limitations)
- PostgreSQL gratuit inclus
- SSL gratuit
- Déploiement depuis GitHub

**Étapes:**

1. **Créer un compte sur Render**
   - Allez sur https://render.com/
   - Connectez-vous avec GitHub

2. **Créer le fichier render.yaml**
   ```yaml
   services:
     - type: web
       name: notification-campus
       env: docker
       dockerfilePath: ./Dockerfile
       envVars:
         - key: SECRET_KEY
           generateValue: true
         - key: DEBUG
           value: False
         - key: DATABASE_URL
           fromDatabase:
             name: notificationdb
             property: connectionString
         - key: ALLOWED_HOSTS
           value: .onrender.com

   databases:
     - name: notificationdb
       databaseName: notifications
       user: notifuser
   ```

3. **Créer un nouveau Web Service**
   - "New" → "Web Service"
   - Connectez votre repo GitHub
   - Render détectera automatiquement le Dockerfile

4. **Configurer**
   - Build Command: (laissez vide, Docker s'en charge)
   - Start Command: `gunicorn systeme_notification.wsgi:application --bind 0.0.0.0:$PORT`

5. **Ajouter PostgreSQL**
   - "New" → "PostgreSQL"
   - Copiez le "Internal Database URL"
   - Ajoutez-le dans les variables d'environnement du web service

6. **Déployer**
   - Votre app sera sur: https://votre-app.onrender.com

---

### Option 3: Fly.io 🚁

**Avantages:**
- Gratuit jusqu'à 3 petites apps
- Déploiement rapide
- Support Docker natif

**Étapes:**

1. **Installer Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex

   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Se connecter**
   ```bash
   fly auth login
   ```

3. **Créer le fichier fly.toml**
   ```toml
   app = "notification-campus"
   primary_region = "cdg"

   [build]
     dockerfile = "Dockerfile"

   [env]
     PORT = "8000"

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0

   [[services]]
     protocol = "tcp"
     internal_port = 8000
     
     [[services.ports]]
       port = 80
       handlers = ["http"]
     
     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

4. **Lancer l'app**
   ```bash
   fly launch
   ```

5. **Ajouter PostgreSQL**
   ```bash
   fly postgres create
   fly postgres attach --app notification-campus
   ```

6. **Configurer les secrets**
   ```bash
   fly secrets set SECRET_KEY=votre-secret-key
   fly secrets set DEBUG=False
   ```

7. **Déployer**
   ```bash
   fly deploy
   ```

---

### Option 4: PythonAnywhere (Limité)

**Gratuit mais limité:**
- Pas de support Docker
- 1 web app gratuite
- Pas de PostgreSQL gratuit (SQLite seulement)

Non recommandé pour ce projet.

---

## 📦 Préparer le déploiement

### 1. Créer les fichiers de configuration

J'ai déjà créé:
- ✅ Dockerfile
- ✅ docker-compose.yml
- ✅ .env.example
- ✅ nginx.conf

### 2. Mettre à jour requirements.txt
```bash
pip freeze > requirements.txt
```

### 3. Créer .gitignore
```
.env
*.pyc
__pycache__/
db.sqlite3
notifsysdb.sqlite3
staticfiles/
```

### 4. Tester en local
```bash
docker-compose up --build
```

---

## 🔐 Sécurité - Variables d'environnement

**Ne JAMAIS commiter:**
- `.env` (contient les secrets)
- Clés API
- Mots de passe

**Toujours utiliser:**
- `.env.example` (template sans valeurs sensibles)
- Variables d'environnement sur la plateforme d'hébergement

---

## 🎯 Recommandation finale

**Pour votre projet, je recommande Railway:**

1. **Plus simple** à configurer
2. **PostgreSQL inclus** gratuitement
3. **5$ gratuit/mois** (suffisant pour une petite app)
4. **Déploiement automatique** depuis GitHub
5. **Logs en temps réel**

**Ordre de préférence:**
1. 🥇 Railway (le plus simple)
2. 🥈 Render (vraiment gratuit, mais plus lent)
3. 🥉 Fly.io (plus technique, bon pour apprendre)

---

## 📝 Checklist avant déploiement

- [ ] `.env` ajouté dans `.gitignore`
- [ ] `SECRET_KEY` changée en production
- [ ] `DEBUG=False` en production
- [ ] `ALLOWED_HOSTS` configuré
- [ ] Base de données PostgreSQL configurée
- [ ] `python manage.py collectstatic` exécuté
- [ ] `python manage.py migrate` exécuté
- [ ] Superuser créé

---

## 🆘 Dépannage

### Erreur "Bad Request (400)"
→ Ajoutez votre domaine dans `ALLOWED_HOSTS`

### Erreur de base de données
→ Vérifiez `DATABASE_URL` dans les variables d'environnement

### Fichiers statiques non chargés
→ Exécutez `python manage.py collectstatic`

### Application ne démarre pas
→ Vérifiez les logs de la plateforme

---

## 📞 Support

Consultez la documentation de chaque plateforme:
- Railway: https://docs.railway.app/
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs/

---

**Créé pour:** Système de Notifications Campus  
**Version:** 1.0 Docker  
**Date:** 2025

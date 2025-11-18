# 🔔 Système de Notifications Campus

Système de notifications d'urgence pour campus universitaire avec dashboards utilisateur et administrateur.

**🆕 Nouveau:** Configuration Docker complète pour hébergement gratuit!

---

## ✨ Résumé complet

J'ai créé pour vous:
- ✅ **17 fichiers Docker** pour le déploiement
- ✅ **3 configurations** d'hébergement gratuit (Railway, Render, Fly.io)
- ✅ **Settings.py adapté** pour la production
- ✅ **Scripts d'aide** pour faciliter le déploiement
- ✅ **Documentation complète** étape par étape

---

## 🚀 Déploiement en 5 minutes

### Étape 1: Préparation
```bash
# Créer .env
cp .env.example .env

# Générer SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(50))"
# Copiez la clé générée dans .env
```

### Étape 2: Push sur GitHub
```bash
git init
git add .
git commit -m "Add Docker configuration"
git branch -M main
git remote add origin https://github.com/votre-username/votre-repo.git
git push -u origin main
```

### Étape 3: Déployer sur Railway (RECOMMANDÉ)
1. Allez sur **https://railway.app/**
2. Connectez-vous avec GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Sélectionnez votre repository
5. Cliquez **+ New** → **Database** → **PostgreSQL**
6. Dans votre service web, allez dans **Variables** et ajoutez:
   ```
   SECRET_KEY = (votre clé générée)
   DEBUG = False
   ALLOWED_HOSTS = *.railway.app
   DATABASE_URL = ${{Postgres.DATABASE_URL}}
   ```
7. **Generate Domain**

**C'est déployé! 🎉** Votre app est en ligne sur `https://votre-app.railway.app`

---

## 🆓 Options d'hébergement gratuit

### 🥇 Railway (Recommandé)
- **Gratuit:** 5$/mois (amplement suffisant)
- **PostgreSQL:** Inclus gratuitement
- **SSL:** Automatique
- **Facilité:** ⭐⭐⭐⭐⭐

### 🥈 Render
- **Gratuit:** 100% gratuit
- **PostgreSQL:** Inclus
- **Note:** App s'endort après 15min d'inactivité
- **Facilité:** ⭐⭐⭐⭐

### 🥉 Fly.io
- **Gratuit:** 3 apps
- **PostgreSQL:** Séparé
- **Note:** Plus technique (CLI)
- **Facilité:** ⭐⭐⭐

---

## 📚 Documentation créée

### Guides de déploiement
1. **[DEPLOY_QUICKSTART.md](DEPLOY_QUICKSTART.md)** - Déploiement en 5 minutes ⚡
2. **[DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)** - Guide complet Docker + hébergement 📖
3. **[DOCKER_SUMMARY.md](DOCKER_SUMMARY.md)** - Vue d'ensemble et comparaison 📊

### Dashboards (déjà créés)
4. **[QUICKSTART.md](QUICKSTART.md)** - Dashboards en local
5. **[DASHBOARD_README.md](DASHBOARD_README.md)** - Doc complète dashboards
6. **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Résumé installation

---

## 🐳 Fichiers Docker créés

### Configuration principale
- ✅ **Dockerfile** - Image Docker de l'application
- ✅ **docker-compose.yml** - Orchestration (Django, PostgreSQL, Redis, Nginx)
- ✅ **.env.example** - Template des variables d'environnement
- ✅ **nginx.conf** - Configuration du reverse proxy
- ✅ **.dockerignore** - Exclusions Docker

### Configurations plateformes
- ✅ **railway.json** - Configuration Railway
- ✅ **render.yaml** - Configuration Render
- ✅ **fly.toml** - Configuration Fly.io

### Outils
- ✅ **prepare_deploy.py** - Vérification avant déploiement
- ✅ **deploy.bat** - Assistant Windows interactif
- ✅ **.gitignore** - Fichiers à exclure
- ✅ **requirements_clean.txt** - Dépendances propres

### Code adapté
- ✅ **settings.py** - Modifié pour production (variables d'env, PostgreSQL, WhiteNoise)

---

## 💻 Test en local avec Docker

```bash
# 1. Créer .env
cp .env.example .env

# 2. Modifier .env avec votre SECRET_KEY

# 3. Démarrer Docker
docker-compose up --build

# 4. Dans un autre terminal - Migrations
docker-compose exec web python manage.py migrate

# 5. Créer superuser
docker-compose exec web python manage.py createsuperuser

# 6. Créer données de démo (optionnel)
docker-compose exec web python create_demo_data.py

# 7. Accéder
# http://localhost
# http://localhost/dashboard/
# http://localhost/admin/
```

**Arrêter:**
```bash
docker-compose down
```

---

## 🛠️ Scripts d'aide

### Windows: Assistant interactif
```bash
deploy.bat
```
Menu avec options:
1. Créer le fichier .env
2. Tester avec Docker
3. Préparer pour GitHub
4. Afficher les instructions

### Python: Vérification
```bash
python prepare_deploy.py
```
- Vérifie tous les fichiers
- Génère une SECRET_KEY
- Affiche les instructions

---

## 📋 Checklist déploiement

**Avant:**
- [ ] Code sur GitHub
- [ ] `.env` dans `.gitignore` ✅
- [ ] SECRET_KEY générée
- [ ] Testé en local (optionnel)

**Sur la plateforme:**
- [ ] Service créé
- [ ] PostgreSQL ajouté
- [ ] Variables configurées
- [ ] Domaine généré
- [ ] Migrations exécutées
- [ ] Superuser créé

---

## 🎯 Fonctionnalités

### Dashboards
- ✅ Dashboard utilisateur avec notifications personnelles
- ✅ Dashboard admin avec statistiques globales
- ✅ Graphiques interactifs (Chart.js)
- ✅ Actualisation en temps réel

### Système de notifications
- ✅ Notifications personnalisées par utilisateur
- ✅ Priorités (haute, moyenne, faible)
- ✅ Système d'évacuation d'urgence
- ✅ API REST complète

---

## 🌐 URLs

| URL | Description | Accès |
|-----|-------------|-------|
| `/dashboard/` | Dashboard utilisateur | Utilisateur connecté |
| `/dashboard/admin/` | Dashboard administrateur | Superuser |
| `/api/notifications/` | API notifications | Token/Session |
| `/api/stats/` | API statistiques | Token/Session |
| `/admin/` | Interface admin Django | Superuser |

---

## 🛡️ Sécurité

**En production:**
- ✅ `DEBUG=False`
- ✅ SECRET_KEY unique
- ✅ PostgreSQL (pas SQLite)
- ✅ HTTPS automatique
- ✅ Variables d'environnement

**Générer SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 🆘 Problèmes courants

### "Bad Request (400)"
→ Ajoutez votre domaine dans `ALLOWED_HOSTS`

### Base de données non trouvée
→ Vérifiez `DATABASE_URL` dans les variables

### Fichiers statiques ne chargent pas
→ Exécutez `python manage.py collectstatic --noinput`

### App ne démarre pas
→ Consultez les logs de la plateforme

---

## 🎉 Résultat final

Après déploiement, vous aurez:
- 🌐 **Application en ligne 24/7**
- 🆓 **Hébergement gratuit**
- 🔒 **HTTPS automatique**
- 📊 **Dashboards accessibles**
- 🗄️ **PostgreSQL gratuit**
- 📈 **Scalable**

---

## 📞 Support

### Documentation
- **DEPLOY_QUICKSTART.md** - Guide ultra-rapide
- **DOCKER_DEPLOY.md** - Guide complet
- **DOCKER_SUMMARY.md** - Comparaison des options

### Liens utiles
- Railway: https://docs.railway.app/
- Render: https://render.com/docs
- Fly.io: https://fly.io/docs/
- Django: https://docs.djangoproject.com/

---

**Version:** 1.0 Docker Ready  
**Status:** ✅ Production Ready  
**Hébergement:** 🆓 Gratuit  
**Date:** 2025

**Votre application est prête pour le cloud! 🚀**

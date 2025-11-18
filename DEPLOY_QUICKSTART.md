# 🚀 Guide Rapide - Déploiement Gratuit

## ✅ Ce qui a été créé

### Fichiers Docker
- ✅ `Dockerfile` - Image Docker de l'application
- ✅ `docker-compose.yml` - Services (Django, PostgreSQL, Redis, Nginx)
- ✅ `.env.example` - Template des variables d'environnement
- ✅ `nginx.conf` - Configuration Nginx
- ✅ `.dockerignore` - Exclusions Docker

### Fichiers de déploiement
- ✅ `railway.json` - Configuration Railway
- ✅ `render.yaml` - Configuration Render
- ✅ `fly.toml` - Configuration Fly.io
- ✅ `.gitignore` - Fichiers à exclure de Git
- ✅ `requirements_clean.txt` - Dépendances propres

### Code modifié
- ✅ `settings.py` - Adapté pour production (variables d'environnement, PostgreSQL, whitenoise)

---

## 🎯 Option recommandée: Railway

**C'est la plus simple!**

### Étape 1: Préparation

1. **Pusher votre code sur GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Add Docker configuration"
   git branch -M main
   git remote add origin https://github.com/votre-username/votre-repo.git
   git push -u origin main
   ```

2. **Créer un fichier .env local (ne pas commiter!):**
   ```bash
   cp .env.example .env
   ```

### Étape 2: Déploiement Railway

1. **Allez sur https://railway.app/**

2. **Connectez-vous avec GitHub**

3. **Créez un nouveau projet:**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre repository

4. **Ajoutez PostgreSQL:**
   - Dans le projet, cliquez "+ New"
   - Sélectionnez "Database" → "Add PostgreSQL"
   - Railway crée automatiquement la DB

5. **Configurez les variables:**
   - Cliquez sur votre service web
   - Allez dans "Variables"
   - Ajoutez:
     ```
     SECRET_KEY = (générez une clé sécurisée)
     DEBUG = False
     ALLOWED_HOSTS = *.railway.app
     DATABASE_URL = ${{Postgres.DATABASE_URL}}
     ```

6. **Déployez:**
   - Railway déploie automatiquement
   - Attendez que le build se termine (3-5 min)

7. **Exécutez les migrations:**
   Dans l'onglet "Settings" de votre service, ajoutez ce "Deploy Command":
   ```
   python manage.py migrate && python manage.py collectstatic --noinput
   ```

8. **Créez un superuser:**
   Dans l'onglet "Terminal" du service:
   ```bash
   python manage.py createsuperuser
   ```

9. **Accédez à votre app:**
   - Cliquez sur "Settings" → "Generate Domain"
   - Votre app est sur: `https://votre-app.railway.app`

**Coût:** 5$ gratuit/mois (suffisant!)

---

## 🆓 Alternative: Render (100% gratuit)

### Étape 1: Préparation

Même chose que Railway (push sur GitHub)

### Étape 2: Déploiement Render

1. **Allez sur https://render.com/**

2. **Créez un compte (GitHub)**

3. **Créez un nouveau Web Service:**
   - "New" → "Web Service"
   - Connectez votre repo
   - Render détecte le Dockerfile

4. **Configuration:**
   - Name: `notification-campus`
   - Environment: `Docker`
   - Instance Type: `Free`

5. **Variables d'environnement:**
   ```
   SECRET_KEY = (générez une clé)
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   ```

6. **Ajoutez PostgreSQL:**
   - "New" → "PostgreSQL"
   - Name: `notificationdb`
   - Copiez l'"Internal Database URL"
   - Retournez au Web Service
   - Ajoutez variable: `DATABASE_URL = (collez l'URL)`

7. **Déployez:**
   - Cliquez "Create Web Service"
   - Attendez 5-10 minutes (premier déploiement lent)

8. **Exécutez les migrations:**
   Dans le "Shell" du service:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

9. **Accédez:**
   - `https://votre-app.onrender.com`

**Coût:** Gratuit! (mais l'app s'endort après 15 min d'inactivité)

---

## 🧪 Test en local avec Docker

Avant de déployer, testez en local:

```bash
# 1. Créer le .env
cp .env.example .env

# 2. Lancer Docker
docker-compose up --build

# 3. Dans un autre terminal - Migrations
docker-compose exec web python manage.py migrate

# 4. Créer superuser
docker-compose exec web python manage.py createsuperuser

# 5. Accéder
# http://localhost
```

---

## 🔐 Générer une SECRET_KEY sécurisée

Python:
```python
import secrets
print(secrets.token_urlsafe(50))
```

Ou en ligne de commande:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 📋 Checklist avant déploiement

- [ ] Code pushé sur GitHub
- [ ] `.env` dans `.gitignore`
- [ ] SECRET_KEY générée et sécurisée
- [ ] DEBUG=False en production
- [ ] ALLOWED_HOSTS configuré
- [ ] PostgreSQL configuré
- [ ] Testé en local avec Docker

---

## 🆘 Problèmes courants

### "Bad Request (400)"
→ Ajoutez votre domaine dans `ALLOWED_HOSTS`

### "DisallowedHost"
→ Même chose, vérifiez `ALLOWED_HOSTS`

### Base de données non trouvée
→ Vérifiez que `DATABASE_URL` est bien configuré

### Fichiers statiques non chargés
→ `python manage.py collectstatic --noinput`

### App ne démarre pas
→ Consultez les logs sur la plateforme

---

## 📞 Ressources

- **Railway:** https://docs.railway.app/
- **Render:** https://render.com/docs
- **Django Production:** https://docs.djangoproject.com/en/5.2/howto/deployment/

---

## 🎉 Félicitations!

Votre application est maintenant prête pour le cloud! 

**Prochaines étapes:**
1. Tester localement avec Docker
2. Choisir une plateforme (Railway recommandé)
3. Déployer
4. Créer un superuser
5. Profiter!

**Votre app sera accessible 24/7 gratuitement!** 🚀

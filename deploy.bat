@echo off
chcp 65001 >nul
cls

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║          🚀 PRÉPARATION AU DÉPLOIEMENT DOCKER 🐳              ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Vérification Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

echo ✅ Python détecté
echo.

echo 📋 Vérification des fichiers Docker...
python prepare_deploy.py

if errorlevel 1 (
    echo.
    echo ❌ Certains fichiers sont manquants
    pause
    exit /b 1
)

echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎯 Que voulez-vous faire?
echo.
echo 1. Créer le fichier .env
echo 2. Tester avec Docker (docker-compose up)
echo 3. Préparer pour GitHub
echo 4. Afficher les instructions complètes
echo 5. Quitter
echo.
set /p CHOICE="Votre choix (1-5): "

if "%CHOICE%"=="1" goto CREATE_ENV
if "%CHOICE%"=="2" goto TEST_DOCKER
if "%CHOICE%"=="3" goto PREPARE_GIT
if "%CHOICE%"=="4" goto SHOW_INSTRUCTIONS
if "%CHOICE%"=="5" goto END
goto MENU

:CREATE_ENV
echo.
echo 📝 Création du fichier .env...
if exist .env (
    echo ⚠️  Le fichier .env existe déjà!
    set /p OVERWRITE="Voulez-vous l'écraser? (O/N): "
    if /i not "%OVERWRITE%"=="O" goto MENU
)
copy .env.example .env
echo ✅ Fichier .env créé!
echo.
echo 💡 N'oubliez pas de modifier SECRET_KEY dans .env
echo    Utilisez la clé générée ci-dessus.
pause
goto MENU

:TEST_DOCKER
echo.
echo 🐳 Démarrage de Docker...
echo.
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose n'est pas installé
    echo    Téléchargez Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    goto MENU
)

echo ✅ Docker Compose détecté
echo.
if not exist .env (
    echo ⚠️  Fichier .env manquant!
    set /p CREATE="Voulez-vous le créer maintenant? (O/N): "
    if /i "%CREATE%"=="O" goto CREATE_ENV
    goto MENU
)

echo 🚀 Lancement de docker-compose up --build...
echo    (Appuyez sur Ctrl+C pour arrêter)
echo.
docker-compose up --build
goto MENU

:PREPARE_GIT
echo.
echo 📦 Préparation pour GitHub...
echo.
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git n'est pas installé
    echo    Téléchargez Git: https://git-scm.com/downloads
    pause
    goto MENU
)

echo ✅ Git détecté
echo.
echo Commandes à exécuter:
echo.
echo    git init
echo    git add .
echo    git commit -m "Add Docker configuration"
echo    git branch -M main
echo    git remote add origin https://github.com/votre-username/votre-repo.git
echo    git push -u origin main
echo.
set /p EXEC="Voulez-vous exécuter ces commandes maintenant? (O/N): "
if /i not "%EXEC%"=="O" goto MENU

echo.
git init
git add .
git commit -m "Add Docker configuration and deployment files"
git branch -M main

echo.
echo 📝 Entrez l'URL de votre repository GitHub:
set /p REPO_URL="URL (https://github.com/username/repo.git): "
git remote add origin %REPO_URL%
git push -u origin main

echo.
echo ✅ Code poussé sur GitHub!
pause
goto MENU

:SHOW_INSTRUCTIONS
echo.
echo 📚 Instructions complètes:
echo.
echo 1️⃣  RAILWAY (Recommandé):
echo    • https://railway.app/
echo    • New Project → Deploy from GitHub repo
echo    • Ajoutez PostgreSQL
echo    • Configurez les variables d'environnement
echo.
echo 2️⃣  RENDER (100%% gratuit):
echo    • https://render.com/
echo    • New Web Service
echo    • Connectez votre repo GitHub
echo    • Ajoutez PostgreSQL
echo.
echo 3️⃣  FLY.IO:
echo    • Installez Fly CLI
echo    • fly launch
echo    • fly postgres create
echo.
echo 📖 Pour plus de détails:
echo    • DEPLOY_QUICKSTART.md
echo    • DOCKER_DEPLOY.md
echo.
pause
goto MENU

:MENU
echo.
goto START

:END
echo.
echo ✨ Au revoir!
echo.
exit /b 0

:START
cls
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║          🚀 PRÉPARATION AU DÉPLOIEMENT DOCKER 🐳              ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🎯 Que voulez-vous faire?
echo.
echo 1. Créer le fichier .env
echo 2. Tester avec Docker (docker-compose up)
echo 3. Préparer pour GitHub
echo 4. Afficher les instructions complètes
echo 5. Quitter
echo.
set /p CHOICE="Votre choix (1-5): "

if "%CHOICE%"=="1" goto CREATE_ENV
if "%CHOICE%"=="2" goto TEST_DOCKER
if "%CHOICE%"=="3" goto PREPARE_GIT
if "%CHOICE%"=="4" goto SHOW_INSTRUCTIONS
if "%CHOICE%"=="5" goto END
goto START

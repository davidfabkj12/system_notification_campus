#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de préparation au déploiement
Vérifie que tout est prêt pour le déploiement
"""

import os
import sys
import secrets

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_file(filepath, description):
    """Vérifie l'existence d'un fichier"""
    if os.path.exists(filepath):
        print(f"   ✅ {description}")
        return True
    else:
        print(f"   ❌ {description} - MANQUANT")
        return False

def generate_secret_key():
    """Génère une SECRET_KEY sécurisée"""
    return secrets.token_urlsafe(50)

def main():
    print_header("🚀 PRÉPARATION AU DÉPLOIEMENT")
    
    all_ok = True
    
    # Vérifier les fichiers Docker
    print("🐳 Fichiers Docker:")
    all_ok &= check_file('Dockerfile', 'Dockerfile')
    all_ok &= check_file('docker-compose.yml', 'docker-compose.yml')
    all_ok &= check_file('.dockerignore', '.dockerignore')
    all_ok &= check_file('nginx.conf', 'nginx.conf')
    
    # Vérifier les fichiers de configuration
    print("\n📝 Fichiers de configuration:")
    all_ok &= check_file('.env.example', '.env.example')
    all_ok &= check_file('.gitignore', '.gitignore')
    all_ok &= check_file('requirements_clean.txt', 'requirements_clean.txt')
    
    # Vérifier les fichiers de déploiement
    print("\n☁️  Fichiers de déploiement:")
    all_ok &= check_file('railway.json', 'railway.json')
    all_ok &= check_file('render.yaml', 'render.yaml')
    all_ok &= check_file('fly.toml', 'fly.toml')
    
    # Vérifier le fichier .env
    print("\n🔐 Configuration locale:")
    if os.path.exists('.env'):
        print("   ✅ Fichier .env existe")
    else:
        print("   ⚠️  Fichier .env n'existe pas")
        print("   💡 Créez-le avec: cp .env.example .env")
    
    # Générer une nouvelle SECRET_KEY
    print("\n🔑 SECRET_KEY:")
    new_secret = generate_secret_key()
    print(f"   Nouvelle clé générée: {new_secret[:20]}...")
    print(f"   Clé complète: {new_secret}")
    
    # Instructions
    print_header("📋 PROCHAINES ÉTAPES")
    
    if all_ok:
        print("✅ Tous les fichiers sont présents!\n")
        
        print("1️⃣  Créer/Mettre à jour .env:")
        print("   cp .env.example .env")
        print(f"   Remplacez SECRET_KEY par: {new_secret}\n")
        
        print("2️⃣  Tester en local avec Docker:")
        print("   docker-compose up --build\n")
        
        print("3️⃣  Pousser sur GitHub:")
        print("   git init")
        print("   git add .")
        print('   git commit -m "Add Docker configuration"')
        print("   git branch -M main")
        print("   git remote add origin https://github.com/username/repo.git")
        print("   git push -u origin main\n")
        
        print("4️⃣  Déployer sur Railway:")
        print("   • Allez sur https://railway.app/")
        print("   • New Project → Deploy from GitHub repo")
        print("   • Ajoutez PostgreSQL")
        print("   • Configurez les variables d'environnement")
        print(f"     SECRET_KEY = {new_secret}")
        print("     DEBUG = False")
        print("     ALLOWED_HOSTS = *.railway.app")
        print("     DATABASE_URL = ${{Postgres.DATABASE_URL}}\n")
        
        print("📚 Documentation complète:")
        print("   • DEPLOY_QUICKSTART.md - Guide rapide")
        print("   • DOCKER_DEPLOY.md - Guide complet")
        
    else:
        print("⚠️  CERTAINS FICHIERS SONT MANQUANTS\n")
        print("Exécutez d'abord les scripts de création des fichiers Docker.")
    
    print("\n" + "="*70 + "\n")
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

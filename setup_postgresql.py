#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de configuration PostgreSQL
Vérifie et guide pour la configuration PostgreSQL
"""

import os
import sys

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_env_file():
    """Vérifie si .env existe"""
    if os.path.exists('.env'):
        print("✅ Fichier .env trouvé")
        
        # Lire le contenu
        with open('.env', 'r') as f:
            content = f.read()
            
        if 'DATABASE_URL' in content:
            print("✅ DATABASE_URL configuré dans .env")
            
            # Extraire l'URL (sans afficher le mot de passe)
            for line in content.split('\n'):
                if line.startswith('DATABASE_URL'):
                    url = line.split('=', 1)[1].strip()
                    if url.startswith('postgresql://'):
                        # Masquer le mot de passe
                        parts = url.split('@')
                        if len(parts) == 2:
                            print(f"   URL: postgresql://***:***@{parts[1]}")
                        else:
                            print(f"   URL: {url[:30]}...")
                    else:
                        print(f"   ⚠️  DATABASE_URL ne commence pas par postgresql://")
            return True
        else:
            print("⚠️  DATABASE_URL non trouvé dans .env")
            return False
    else:
        print("❌ Fichier .env non trouvé")
        return False

def main():
    print_header("🐘 CONFIGURATION POSTGRESQL")
    
    print("Vérification de la configuration actuelle...\n")
    
    # Vérifier .env
    print("📝 Fichier .env:")
    env_ok = check_env_file()
    
    if not env_ok:
        print("\n" + "="*70)
        print("CONFIGURATION NÉCESSAIRE")
        print("="*70 + "\n")
        
        print("Choisissez votre méthode de configuration:\n")
        print("1️⃣  Docker (RECOMMANDÉ - Le plus simple)")
        print("2️⃣  Cloud (Railway/Render)")
        print("3️⃣  Installation locale\n")
        
        choice = input("Votre choix (1-3): ").strip()
        
        if choice == "1":
            print_docker_config()
        elif choice == "2":
            print_cloud_config()
        elif choice == "3":
            print_local_config()
        else:
            print("\n❌ Choix invalide")
    else:
        print("\n✅ Configuration PostgreSQL détectée!")
        print("\nProchaines étapes:")
        print("1. Démarrer votre environnement (Docker/Local)")
        print("2. Exécuter: python manage.py migrate")
        print("3. Créer un superuser: python manage.py createsuperuser")
    
    print("\n" + "="*70)
    print("📚 Documentation complète: POSTGRESQL_SETUP.md")
    print("="*70 + "\n")

def print_docker_config():
    print("\n" + "="*70)
    print("🐳 CONFIGURATION DOCKER")
    print("="*70 + "\n")
    
    print("C'est le plus simple! PostgreSQL est déjà configuré.\n")
    
    print("Étapes:\n")
    print("1. Créer .env:")
    print("   cp .env.example .env\n")
    
    print("2. Dans .env, utiliser:")
    print("   DATABASE_URL=postgresql://notifuser:notifpass123@db:5432/notificationdb\n")
    
    print("3. Démarrer Docker:")
    print("   docker-compose up --build\n")
    
    print("4. Migrer:")
    print("   docker-compose exec web python manage.py migrate\n")
    
    print("5. Créer superuser:")
    print("   docker-compose exec web python manage.py createsuperuser\n")
    
    print("✅ TERMINÉ! PostgreSQL est prêt.\n")

def print_cloud_config():
    print("\n" + "="*70)
    print("☁️  CONFIGURATION CLOUD")
    print("="*70 + "\n")
    
    print("Pour Railway:\n")
    print("1. Allez sur https://railway.app/")
    print("2. New Project → GitHub repo")
    print("3. + New → Database → PostgreSQL")
    print("4. Dans Variables:")
    print("   DATABASE_URL = ${{Postgres.DATABASE_URL}}\n")
    
    print("Pour Render:\n")
    print("1. Allez sur https://render.com/")
    print("2. New → PostgreSQL")
    print("3. Copiez 'Internal Database URL'")
    print("4. Dans votre Web Service, ajoutez:")
    print("   DATABASE_URL = (collez l'URL)\n")

def print_local_config():
    print("\n" + "="*70)
    print("💻 CONFIGURATION LOCALE")
    print("="*70 + "\n")
    
    print("Windows:\n")
    print("1. Télécharger: https://www.postgresql.org/download/windows/")
    print("2. Installer PostgreSQL 15 ou 16")
    print("3. Ouvrir PowerShell:\n")
    print("   psql -U postgres")
    print("   CREATE DATABASE notificationdb;")
    print("   CREATE USER notifuser WITH PASSWORD 'votre_mot_de_passe';")
    print("   GRANT ALL PRIVILEGES ON DATABASE notificationdb TO notifuser;")
    print("   \\q\n")
    
    print("4. Dans .env:")
    print("   DATABASE_URL=postgresql://notifuser:votre_mot_de_passe@localhost:5432/notificationdb\n")
    
    print("Linux:\n")
    print("   sudo apt install postgresql")
    print("   sudo -u postgres psql")
    print("   CREATE DATABASE notificationdb;")
    print("   CREATE USER notifuser WITH PASSWORD 'votre_mot_de_passe';")
    print("   GRANT ALL PRIVILEGES ON DATABASE notificationdb TO notifuser;\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

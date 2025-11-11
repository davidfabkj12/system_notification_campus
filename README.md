systeme_notification/                  # Projet Django
├── manage.py
├── systeme_notification/              # Répertoire du projet
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── notifications/                      # Application principale
    ├── __init__.py
    ├── admin.py                        # Administration Django
    ├── apps.py
    ├── models.py                       # Modèles Django (User, Notification, etc.)
    ├── core.py                         # Classes métiers, mixins, décorateurs, métaclasses
    ├── descriptors.py                  # Descripteurs (Email, Phone, Priority, TimeWindow)
    ├── decorators.py                   # Décorateurs de classes et méthodes
    ├── metaclasses.py                  # Métaclasses (NotificationMeta, ChannelMeta, TemplateMeta, ConfigMeta)
    ├── serializers.py                  # Serializers DRF pour API
    ├── api.py                           # ViewSets / APIViews pour DRF
    ├── urls.py                          # Routes API
    └── tests.py                         # Tests unitaires pour tous les concepts

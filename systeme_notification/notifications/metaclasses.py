"""
Définition des métaclasses pour automatiser la génération de code autour
des notifications et de leur configuration. Ces métaclasses ajoutent
dynamiquement des méthodes ou des attributs aux classes qui les utilisent.

Les métaclasses sont un moyen puissant de factoriser et de centraliser
des comportements communs lors de la création de nouvelles classes. Dans
ce module, nous fournissons notamment `NotificationMeta`, qui ajoute
automatiquement des validateurs pour les champs obligatoires, une
description par défaut et un type de notification dérivé du nom de la
classe. Un registre global permet en outre de découvrir les
notificateurs disponibles.
"""

from abc import ABCMeta
from typing import Dict, Type, Callable, Iterable


class NotificationRegistry:
    """
    Registre global des classes de notification.

    Ce registre est utilisé pour stocker et retrouver dynamiquement les
    différents types de notificateurs créés via la métaclasse
    ``NotificationMeta``. L'utilisation d'un registre séparé au lieu
    d'une simple variable globale permet de mieux contrôler l'API et
    d'encapsuler la logique d'enregistrement.
    """
    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: str, klass: Type) -> None:
        cls._registry[name] = klass

    @classmethod
    def get(cls, name: str) -> Type | None:
        return cls._registry.get(name)


class NotificationMeta(ABCMeta):
    """
    Métaclasse qui enrichit automatiquement les classes de notification.

    Les fonctionnalités ajoutées sont les suivantes :

    - Si un attribut ``required_fields`` est présent, une méthode
      ``validate_required_fields`` est générée afin de vérifier que
      toutes les valeurs requises sont renseignées sur une instance.
    - Si aucune description n'est fournie, un attribut ``description``
      est créé avec une valeur basée sur le nom de la classe.
    - L'attribut ``_notification_type`` est ajouté et correspond au
      nom de la classe en minuscules. Cela permet d'identifier
      facilement le type de notificateur.
    - La classe est automatiquement enregistrée dans
      ``NotificationRegistry`` pour une découverte ultérieure.
    """

    @classmethod
    def create_validator(cls, required_fields: Iterable[str]) -> Callable[[object], None]:
        """Crée une fonction de validation pour les champs requis."""
        def validator(self) -> None:
            missing = [field for field in required_fields if getattr(self, field, None) is None]
            if missing:
                missing_str = ', '.join(missing)
                raise ValueError(f"Champ(s) requis manquant(s) : {missing_str}")
        return validator

    def __new__(mcls, name: str, bases: tuple[type, ...], attrs: dict) -> Type:
        # Génération d'un validateur si des champs requis sont définis
        if 'required_fields' in attrs:
            attrs['validate_required_fields'] = mcls.create_validator(attrs['required_fields'])
        # Génération d'une description par défaut
        if 'description' not in attrs:
            attrs['description'] = f"Notificateur de type {name}"
        # Ajout d'un identifiant de type basé sur le nom de la classe
        attrs['_notification_type'] = name.lower()
        # Création effective de la classe
        new_class = super().__new__(mcls, name, bases, attrs)
        # Enregistrement dans le registre global
        NotificationRegistry.register(name, new_class)
        return new_class

class ChannelMeta(type):
    # Création automatique de canaux (SMS, Push, Email)
    def __new__(cls, name, bases, attrs):
        attrs['channel_name'] = name.lower()
        return super().__new__(cls, name, bases, attrs)

class TemplateMeta(type):
    # Génération automatique de templates
    def __new__(cls, name, bases, attrs):
        if 'template_fields' in attrs:
            def render_template(self):
                return f"{name} template: {attrs['template_fields']}"
            attrs['render_template'] = render_template
        return super().__new__(cls, name, bases, attrs)

class ConfigMeta(type):
    # Configuration dynamique et validation
    def __new__(cls, name, bases, attrs):
        if 'config' in attrs and not isinstance(attrs['config'], dict):
            raise ValueError(f"{name} config doit être un dict")
        return super().__new__(cls, name, bases, attrs)

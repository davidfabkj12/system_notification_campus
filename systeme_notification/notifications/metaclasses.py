from abc import ABCMeta
from typing import Dict, Type, Callable, Iterable


class NotificationRegistry:
    _registry: Dict[str, Type] = {}

    @classmethod
    def register(cls, name: str, klass: Type) -> None:
        cls._registry[name] = klass

    @classmethod
    def get(cls, name: str) -> Type | None:
        return cls._registry.get(name)


class NotificationMeta(ABCMeta):
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

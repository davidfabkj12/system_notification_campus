from abc import ABCMeta

global_registry = {}

class NotificationMeta(ABCMeta):  
    def __new__(cls, name, bases, attrs):
        if 'required_fields' in attrs:
            def validate(self):
                for field in attrs['required_fields']:
                    if getattr(self, field, None) is None:
                        raise ValueError(f"Champ requis manquant: {field}")
            attrs['validate'] = validate
        # Enregistrement global
        from .decorators import global_registry
        global_registry[name] = cls
        return super().__new__(cls, name, bases, attrs)

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

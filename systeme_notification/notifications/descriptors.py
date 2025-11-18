import re

class EmailDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__.get('email')

    def __set__(self, instance, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValueError(f"Email invalide: {value}")
        instance.__dict__['email'] = value

class PhoneDescriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('phone', instance.phone_db or '+0000000000')

    def __set__(self, instance, value):
        if not re.match(r'^\+\d{10,15}$', value):
            raise ValueError(f"Numéro de téléphone invalide: {value}")
        instance.__dict__['phone'] = value

class PriorityDescriptor:
   
    def __init__(self, default: str = 'faible') -> None:
        # Valeur par défaut si aucune priorité n'est définie
        self.default = default.lower()
        # Jeu des valeurs acceptées (sensible aux minuscules)
        self.allowed_values = {'faible', 'moyenne', 'haute', 'urgente'}

    def __get__(self, instance, owner):
        
        return instance.__dict__.get('priority', self.default)

    def __set__(self, instance, value: str) -> None:
       
        if not isinstance(value, str):
            raise ValueError(f"Priorité invalide : {value} (doit être une chaîne)")
        normalized = value.lower()
        if normalized not in self.allowed_values:
            raise ValueError(
                f"Priorité invalide : {value}. Valeurs autorisées : {', '.join(sorted(self.allowed_values))}"
            )
        instance.__dict__['priority'] = normalized

class TimeWindowDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__.get('time_window')

    def __set__(self, instance, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Time window invalide")
        instance.__dict__['time_window'] = value

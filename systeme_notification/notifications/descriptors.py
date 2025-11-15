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
        return instance.__dict__.get('phone')

    def __set__(self, instance, value):
        if not re.match(r'^\+\d{10,15}$', value):
            raise ValueError(f"Numéro de téléphone invalide: {value}")
        instance.__dict__['phone'] = value

class PriorityDescriptor:
<<<<<<< Updated upstream
    def __init__(self, default='LOW'):
=======
    """
    Descripteur pour la priorité d'une notification ou d'un utilisateur.

    Ce descripteur normalise les valeurs de priorité en s'assurant qu'elles
    appartiennent à un ensemble prédéfini de niveaux. Les niveaux supportés
    sont « faible », « moyenne », « haute » et « urgente ». Si une valeur
    invalide est assignée, une exception est levée. Une valeur par défaut
    peut être passée lors de l'instanciation du descripteur.
    """
    def __init__(self, default: str = 'faible') -> None:
        # Valeur par défaut si aucune priorité n'est définie
>>>>>>> Stashed changes
        self.default = default
        # Jeu des valeurs acceptées (sensible aux minuscules)
        self.allowed_values = {'faible', 'moyenne', 'haute', 'urgente'}

    def __get__(self, instance, owner):
        # Retourne la valeur stockée dans le dictionnaire de l'instance ou
        # la valeur par défaut si elle n'existe pas.
        return instance.__dict__.get('priority', self.default)

<<<<<<< Updated upstream
    def __set__(self, instance, value):
        if value not in ['LOW', 'MEDIUM', 'HIGH', 'URGENT']:
            raise ValueError(f"Priorité invalide: {value}")
        instance.__dict__['priority'] = value
=======
    def __set__(self, instance, value: str) -> None:
        # Normaliser la valeur en chaîne et en minuscules
        if isinstance(value, str):
            normalized = value.lower()
        else:
            raise ValueError(f"Priorité invalide: {value} (doit être une chaîne)")
        if normalized not in self.allowed_values:
            raise ValueError(
                f"Priorité invalide: {value}. Valeurs autorisées: {', '.join(self.allowed_values)}"
            )
        instance.__dict__['priority'] = normalized
>>>>>>> Stashed changes

class TimeWindowDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__.get('time_window')

    def __set__(self, instance, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Time window invalide")
        instance.__dict__['time_window'] = value

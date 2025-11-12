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
    def __init__(self, default='LOW'):
        self.default = default

    def __get__(self, instance, owner):
        return instance.__dict__.get('priority', self.default)

    def __set__(self, instance, value):
        if value not in ['LOW', 'MEDIUM', 'HIGH', 'URGENT']:
            raise ValueError(f"Priorité invalide: {value}")
        instance.__dict__['priority'] = value

class TimeWindowDescriptor:
    def __get__(self, instance, owner):
        return instance.__dict__.get('time_window')

    def __set__(self, instance, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError("Time window invalide")
        instance.__dict__['time_window'] = value

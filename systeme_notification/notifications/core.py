from abc import ABC, abstractmethod
from .decorators import *
from .metaclasses import NotificationMeta

# Mixins
class AlarmMixin:
    @message
    def set_alarm(self):
        return "Alarme activée"

class SpeakerMixin:
    @message
    def speaker(self):
        return "Haut-parleur activé"

class NotificationMixin:
    @message
    def send_notifications(self, message, destinataire=None):
        notif = f"Notification envoyée : {message}"
        print(notif)
        return notif

# # Classe abstraite
# class Urgence(ABC):
#     @abstractmethod
#     def evacuer(self):
#         pass

#     def set_off_alarm(self):
#         print("Alarme désactivée")

# # Sous-classes urgences avec validation corrigée
# @add_performance_tracking
# @auto_configuration_validation   # le décorateur valide maintenant après __init__
# @register_in_global_registry
# @add_circuit_breaker
# class Epidemie(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin, metaclass=NotificationMeta):
#     required_fields = ['nom']
    
#     def __init__(self, nom="Epidemie"):
#         self.nom = nom

#     def evacuer(self):
#         print(f"Evacuation : {self.nom}")
#         self.set_alarm()
#         self.speaker()
#         self.send_notifications("Portez un masque", destinataire=None)

# @add_performance_tracking
# @auto_configuration_validation
# @register_in_global_registry
# @add_circuit_breaker
# class Incendie(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin, metaclass=NotificationMeta):
#     required_fields = ['nom']

#     def __init__(self, nom="Incendie"):
#         self.nom = nom

#     def evacuer(self):
#         print(f"Evacuation : {self.nom}")
#         self.set_alarm()
#         self.speaker()
#         self.send_notifications("Evacuez immédiatement", destinataire=None)

# @add_performance_tracking
# @auto_configuration_validation
# @register_in_global_registry
# @add_circuit_breaker
# class Innondation(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin, metaclass=NotificationMeta):
#     required_fields = ['nom']

#     def __init__(self, nom="Innondation"):
#         self.nom = nom

#     def evacuer(self):
#         print(f"Evacuation : {self.nom}")
#         self.set_alarm()
#         self.speaker()
#         self.send_notifications("Montez à l'étage", destinataire=None)

# @add_performance_tracking
# @auto_configuration_validation
# @register_in_global_registry
# @add_circuit_breaker
# class Securite(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin, metaclass=NotificationMeta):
#     required_fields = ['nom']

#     def __init__(self, nom="Securite"):
#         self.nom = nom

#     def evacuer(self):
#         print(f"Evacuation : {self.nom}")
#         self.set_alarm()
#         self.speaker()
#         self.send_notifications("Suivez les consignes de sécurité", destinataire=None)


from .decorators import (
    AddPerformanceTracking,
    AutoConfigurationValidation,
    RegisterInGlobalRegistry,
    AddCircuitBreaker,
    message
)
from .descriptors import TimeWindowDescriptor


class Urgence:
    time_window = TimeWindowDescriptor()

    def evacuer(self):
        print("Évacuation générique...")


@AddPerformanceTracking()
@AutoConfigurationValidation()
@RegisterInGlobalRegistry()
@AddCircuitBreaker()
class Epidemie(Urgence):
    required_fields = ['nom']

    def __init__(self, nom="Epidemie"):
        self.nom = nom

    @message
    def evacuer(self):
        print(f"Évacuation à cause de {self.nom}")

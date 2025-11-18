from .decorators import (
    AddPerformanceTracking,
    AutoConfigurationValidation,
    RegisterInGlobalRegistry,
    AddCircuitBreaker,
    message
)
from .descriptors import TimeWindowDescriptor

# Mixins pour fonctionnalités transverses
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

# Classe de base pour les urgences
class Urgence:
    time_window = TimeWindowDescriptor()

    def evacuer(self):
        print("Évacuation générique...")

# Exemple de sous-classe Epidemie avec tous les décorateurs appliqués
@AddPerformanceTracking()
@AutoConfigurationValidation()
@RegisterInGlobalRegistry()
@AddCircuitBreaker()
class Epidemie(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin):
    required_fields = ['nom']

    def __init__(self, nom="Epidemie"):
        self.nom = nom

    @message
    def evacuer(self):
        print(f"Évacuation à cause de {self.nom}")
        self.set_alarm()
        self.speaker()
        self.send_notifications("Portez un masque")

# Autres urgences possibles
@AddPerformanceTracking()
@AutoConfigurationValidation()
@RegisterInGlobalRegistry()
@AddCircuitBreaker()
class Incendie(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin):
    required_fields = ['nom']

    def __init__(self, nom="Incendie"):
        self.nom = nom

    @message
    def evacuer(self):
        print(f"Évacuation à cause de {self.nom}")
        self.set_alarm()
        self.speaker()
        self.send_notifications("Evacuez immédiatement")

@AddPerformanceTracking()
@AutoConfigurationValidation()
@RegisterInGlobalRegistry()
@AddCircuitBreaker()
class Innondation(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin):
    required_fields = ['nom']

    def __init__(self, nom="Innondation"):
        self.nom = nom

    @message
    def evacuer(self):
        print(f"Évacuation à cause de {self.nom}")
        self.set_alarm()
        self.speaker()
        self.send_notifications("Montez à l'étage")

@AddPerformanceTracking()
@AutoConfigurationValidation()
@RegisterInGlobalRegistry()
@AddCircuitBreaker()
class Securite(Urgence, AlarmMixin, SpeakerMixin, NotificationMixin):
    required_fields = ['nom']

    def __init__(self, nom="Securite"):
        self.nom = nom

    @message
    def evacuer(self):
        print(f"Évacuation à cause de {self.nom}")
        self.set_alarm()
        self.speaker()
        self.send_notifications("Suivez les consignes de sécurité")

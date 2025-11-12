from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone  
from .descriptors import EmailDescriptor, PhoneDescriptor, PriorityDescriptor, TimeWindowDescriptor

class User(AbstractUser):
    """
    Modèle utilisateur étendu :
    - Email standard Django
    - Email perso, téléphone, priorité, fenêtre temporelle
      avec validation via descripteurs mais stockés en base de données
    """
    email = models.EmailField(unique=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)

    # Champs ORM pour stocker les données
    email_perso_db = models.EmailField(default='perso@domaine.com')
    phone_db = models.CharField(max_length=20, default='+00000000000')
    priority_db = models.CharField(max_length=10, default='LOW')
    time_window_start = models.DateTimeField(default=timezone.now)
    time_window_end = models.DateTimeField(default=timezone.now)

    # Descripteurs pour validation / logique métier
    email_perso = EmailDescriptor()
    phone = PhoneDescriptor()
    priority = PriorityDescriptor()
    time_window = TimeWindowDescriptor()

    # Relations ManyToMany
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    def __init__(self, *args, **kwargs):
        # Extraction des valeurs personnalisées pour les descripteurs
        email_val = kwargs.pop('email_perso', None)
        phone_val = kwargs.pop('phone', None)
        priority_val = kwargs.pop('priority', None)
        time_window_val = kwargs.pop('time_window', None)
        super().__init__(*args, **kwargs)

        # Initialisation des descripteurs avec valeurs fournies ou défauts
        if email_val:
            self.email_perso = email_val
        if phone_val:
            self.phone = phone_val
        if priority_val:
            self.priority = priority_val
        if time_window_val:
            self.time_window = time_window_val
        else:
            # Valeur par défaut timezone-aware pour éviter les warnings
            self.time_window = (self.time_window_start, self.time_window_end)

    def save(self, *args, **kwargs):
        """
        Synchronisation des descripteurs avec les champs ORM avant sauvegarde.
        Cela permet de conserver les valeurs validées en base.
        """
        self.email_perso_db = self.email_perso
        self.phone_db = self.phone
        self.priority_db = self.priority
        self.time_window_start, self.time_window_end = self.time_window
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email} / {self.email_perso})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

# Modèle Notification
class Notification(models.Model):
    message = models.TextField()
    destinataire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.destinataire} : {self.message[:30]}"

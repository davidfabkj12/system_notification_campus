from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from .descriptors import (
    EmailDescriptor,
    PhoneDescriptor,
    PriorityDescriptor,
    TimeWindowDescriptor
)
from datetime import datetime



#utilisateur personnalise 
class User(AbstractUser):
    """
    Modèle utilisateur étendu :
    - Conserve l'email standard Django (champ 'email')
    - Ajoute un email_perso avec un descripteur de validation personnalisé
    - Ajoute un numéro de téléphone et un niveau de priorité (POO)
    - Ajoute une fenêtre temporelle (TimeWindowDescriptor)
    """

    # Champs ORM Django natifs
    email = models.EmailField(unique=True, blank=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Champs additionnels via ORM (stockés en base)
    bio = models.TextField(blank=True, null=True, help_text="Courte biographie optionnelle")

    # Champs logiques via descripteurs
    email_perso = EmailDescriptor()
    phone = PhoneDescriptor()
    priority = PriorityDescriptor(default='LOW')
    time_window = TimeWindowDescriptor()

    # Groupes et permissions (pour éviter le conflit avec auth.User)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="Groupes d'appartenance",
        verbose_name="groupes"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Permissions spécifiques de cet utilisateur",
        verbose_name="permissions utilisateur"
    )

    def __init__(self, *args, **kwargs):
        """
        Initialise les valeurs par défaut des descripteurs.
        """
        super().__init__(*args, **kwargs)
        if not hasattr(self, '_email_perso'):
            self.email_perso = kwargs.get('email_perso', 'perso@domaine.com')
        if not hasattr(self, '_phone'):
            self.phone = kwargs.get('phone', '+00000000000')
        if not hasattr(self, '_priority'):
            self.priority = kwargs.get('priority', 'LOW')
        if not hasattr(self, '_time_window'):
            self.time_window = kwargs.get(
                'time_window',
                (datetime.now(), datetime.now())  # valeur temporaire
            )

    def __str__(self):
        return f"{self.username} ({self.email} / {self.email_perso})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

class Notification(models.Model):
    message = models.TextField()
    destinataire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.destinataire} : {self.message[:30]}"

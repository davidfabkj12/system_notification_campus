from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from .descriptors import EmailDescriptor, PhoneDescriptor


# ------------------------------
# Custom User Manager
# ------------------------------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Le username doit être défini')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Champs personnalisés par défaut
        extra_fields.setdefault('phone', '+0000000000')
        extra_fields.setdefault('email_perso', 'perso@domaine.com')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# ------------------------------
# Custom User
# ------------------------------
class User(AbstractUser):
    """
    Modèle utilisateur étendu basé sur AbstractUser.
    On retire priority et time_window, ils seront gérés via Notification.
    """

    # Champs ORM pour stockage réel
    phone_db = models.CharField(max_length=20, default='+0000000000', blank=True)
    email_perso_db = models.EmailField(default='perso@domaine.com', blank=True)
    bio = models.TextField(blank=True, null=True)
    time_window_start = models.DateTimeField(default=timezone.now)
    time_window_end = models.DateTimeField(default=timezone.now)

    # Descripteurs restants pour validation
    email_perso = EmailDescriptor()
    phone = PhoneDescriptor()

    # Relations ManyToMany pour groupes et permissions
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

    # Manager personnalisé
    objects = CustomUserManager()

    def __init__(self, *args, **kwargs):
        email_val = kwargs.pop('email_perso', None)
        phone_val = kwargs.pop('phone', None)
        super().__init__(*args, **kwargs)

        if email_val:
            self.email_perso = email_val
        if phone_val:
            self.phone = phone_val

    def save(self, *args, **kwargs):
        # Synchronisation des champs ORM avec les descripteurs
        self.email_perso_db = self.email_perso
        self.phone_db = self.phone
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email} / {self.email_perso})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


# ------------------------------
# Modèle Notification
# ------------------------------
class Notification(models.Model):
    message = models.TextField()
    destinataire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Champs hérités automatiquement depuis l’utilisateur
    priority = models.CharField(max_length=10, default='LOW')
    time_window_start = models.DateTimeField(null=True, blank=True)
    time_window_end = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.destinataire:
            # Copier priority et time_window depuis l'utilisateur
            self.priority = getattr(self.destinataire, 'priority', 'LOW')
            self.time_window_start = self.destinataire.time_window_start
            self.time_window_end = self.destinataire.time_window_end
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification to {self.destinataire} [{self.priority}] : {self.message[:30]}"
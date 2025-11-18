from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
from .descriptors import EmailDescriptor, PhoneDescriptor, PriorityDescriptor, TimeWindowDescriptor


# Custom User Manager
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



# Custom User
class User(AbstractUser):
    # Champs ORM pour stockage réel
    phone_db = models.CharField(max_length=20, default='+0000000000', blank=True)
    email_perso_db = models.EmailField(default='perso@domaine.com', blank=True)
    bio = models.TextField(blank=True, null=True)
    time_window_start = models.DateTimeField(default=timezone.now)
    time_window_end = models.DateTimeField(default=timezone.now)
    priority_db = models.CharField(max_length=10, default='faible', blank=True)

    # Descripteurs restants pour validation
    email_perso = EmailDescriptor()
    phone = PhoneDescriptor()

    # Descripteur pour la priorité de l'utilisateur. Permet de valider et
    priority = PriorityDescriptor()

    # Descripteur pour la fenêtre temporelle (start, end). Lors de
    time_window = TimeWindowDescriptor()

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
        priority_val = kwargs.pop('priority', None)
        time_window_val = kwargs.pop('time_window', None)
        super().__init__(*args, **kwargs)

        if email_val:
            self.email_perso = email_val
        if phone_val:
            self.phone = phone_val
        if priority_val:
            # Le descripteur ``priority`` s'assure que la valeur est valide
            self.priority = priority_val
        if time_window_val:
            # Affecte la fenêtre temporelle si fournie lors de l'instanciation
            self.time_window = time_window_val

    def save(self, *args, **kwargs):
        # Synchronisation des champs ORM avec les descripteurs
        self.email_perso_db = self.email_perso
        self.phone_db = self.phone
        # Synchroniser la priorité et la plage horaire depuis les descripteurs
        self.priority_db = self.priority
        # Si une fenêtre temporelle a été définie via le descripteur,
        if 'time_window' in self.__dict__:
            tw = self.__dict__['time_window']
            if isinstance(tw, tuple) and len(tw) == 2:
                self.time_window_start, self.time_window_end = tw
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.email} / {self.email_perso}) [prio={self.priority}]"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


# Modèle Notification
class Notification(models.Model):
    message = models.TextField()
    destinataire = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    priority = models.CharField(max_length=10, default='faible')
    time_window_start = models.DateTimeField(null=True, blank=True)
    time_window_end = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.destinataire:
            default_priority = self.__class__._meta.get_field('priority').default
            if self.priority is None or self.priority == '' or self.priority == default_priority:
                self.priority = getattr(self.destinataire, 'priority', default_priority)
            # Copier la fenêtre temporelle depuis l'utilisateur
            self.time_window_start = self.destinataire.time_window_start
            self.time_window_end = self.destinataire.time_window_end
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notification to {self.destinataire} [{self.priority}] : {self.message[:30]}"
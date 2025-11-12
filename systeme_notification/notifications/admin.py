from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Notification

class UserAdmin(BaseUserAdmin):
    # Utiliser des méthodes pour exposer descripteurs
    list_display = ('username', 'email', 'get_email_perso', 'get_phone', 'get_priority', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'priority_db')  # filtrer sur champ réel

    search_fields = ('username', 'email', 'email_perso_db', 'phone_db')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'email_perso', 'phone', 'bio', 'priority', 'time_window')
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'email_perso', 'phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    # --- Méthodes pour exposer les descripteurs ---
    def get_email_perso(self, obj):
        return obj.email_perso
    get_email_perso.short_description = 'Email perso'

    def get_phone(self, obj):
        return obj.phone
    get_phone.short_description = 'Téléphone'

    def get_priority(self, obj):
        return obj.priority
    get_priority.short_description = 'Priorité'

# Admin Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'destinataire', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('destinataire__username', 'message')
    ordering = ('-created_at',)

# Enregistrement
admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)

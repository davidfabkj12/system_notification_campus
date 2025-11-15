<<<<<<< Updated upstream
=======
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
import json
>>>>>>> Stashed changes
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .core import Epidemie, Incendie, Innondation, Securite
class CustomLoginView(LoginView):
    """
    Vue de connexion personnalisée.

    Cette classe hérite de ``django.contrib.auth.views.LoginView`` et
    surcharge ``get_success_url`` pour diriger automatiquement les
    administrateurs (super‑utilisateurs) vers leur tableau de bord
    spécifique après authentification. Les utilisateurs normaux sont
    redirigés vers leur propre tableau de bord.
    """

    template_name = 'notifications/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/dashboard/admin/'
        return '/dashboard/'


@login_required
@user_passes_test(lambda u: u.is_superuser)
def broadcast_notifications(request):
    """
    Vue permettant à l'administrateur d'envoyer une notification à tous les utilisateurs.

    Cette vue prend un message via POST, crée une notification pour chaque
    utilisateur et redirige ensuite vers le tableau de bord admin. Seuls
    les super‑utilisateurs peuvent accéder à cette fonctionnalité.
    """
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        priority = request.POST.get('priority', 'moyenne')  # par défaut moyenne
        if message:
            users = User.objects.all()
            notifications = []
            for user in users:
                notif = Notification(destinataire=user, message=message, priority=priority)
                notifications.append(notif)
            # Utilise bulk_create pour améliorer la performance
            Notification.objects.bulk_create(notifications)
        return redirect('admin_dashboard')
    else:
        return redirect('admin_dashboard')

<<<<<<< Updated upstream
=======


@login_required
def user_dashboard(request):
    """
    Tableau de bord de l'utilisateur.

    Cette vue est désormais protégée par le décorateur ``login_required`` afin de
    garantir qu'un utilisateur soit authentifié avant d'accéder à son tableau de
    bord. Sans authentification, Django redirige automatiquement vers
    ``settings.LOGIN_URL`` tout en conservant le paramètre ``next`` pour que
    l'utilisateur soit renvoyé vers le tableau de bord après la connexion.
    """
    user = request.user
    # Récupère les notifications destinées à l'utilisateur connecté.
    notifications = Notification.objects.filter(destinataire=user).order_by('-created_at')

    context = {
        'user': user,
        'notifications': notifications,
        'total_notifications': notifications.count(),
        'unread_notifications': notifications.filter(
            created_at__gte=timezone.now() - timedelta(days=1)
        ).count(),
        'high_priority': notifications.filter(priority='haute').count(),
    }
    return render(request, 'notifications/user_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    """Dashboard pour les administrateurs"""
    # Statistiques générales
    total_users = User.objects.count()
    total_notifications = Notification.objects.count()
    
    # Notifications par priorité
    priority_stats = list(Notification.objects.values('priority').annotate(count=Count('id')))
    
    # Notifications récentes (dernières 24h, 7 jours, 30 jours)
    now = timezone.now()
    notifs_24h = Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count()
    notifs_7d = Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count()
    notifs_30d = Notification.objects.filter(created_at__gte=now - timedelta(days=30)).count()
    
    # Top 5 utilisateurs avec le plus de notifications
    top_users = User.objects.annotate(
        notif_count=Count('notification')
    ).order_by('-notif_count')[:5]
    
    # Notifications récentes
    recent_notifications = Notification.objects.all().order_by('-created_at')[:10]
    
    # Distribution par jour (derniers 7 jours)
    daily_stats = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = Notification.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end
        ).count()
        daily_stats.append({
            'date': day_start.strftime('%d/%m'),
            'count': count
        })
    daily_stats.reverse()
    
    context = {
        'total_users': total_users,
        'total_notifications': total_notifications,
        'priority_stats': priority_stats,
        'notifs_24h': notifs_24h,
        'notifs_7d': notifs_7d,
        'notifs_30d': notifs_30d,
        'top_users': top_users,
        'recent_notifications': recent_notifications,
        'daily_stats': json.dumps(daily_stats),
    }
    return render(request, 'notifications/admin_dashboard.html', context)


@api_view(['GET'])
def stats_api(request):
    """API pour obtenir les statistiques en temps réel"""
    now = timezone.now()
    
    stats = {
        'total_users': User.objects.count(),
        'total_notifications': Notification.objects.count(),
        'notifs_24h': Notification.objects.filter(created_at__gte=now - timedelta(hours=24)).count(),
        'notifs_7d': Notification.objects.filter(created_at__gte=now - timedelta(days=7)).count(),
        'priority_counts': {
            'haute': Notification.objects.filter(priority='haute').count(),
            'moyenne': Notification.objects.filter(priority='moyenne').count(),
            'faible': Notification.objects.filter(priority='faible').count(),
        }
    }
    return Response(stats)


>>>>>>> Stashed changes
class EvacuationViewSet(viewsets.ViewSet):
    # GET /api/evacuation/epidemie/
    @action(detail=False, methods=["get"])
    def epidemie(self, request):
        return Response({"message": "Évacuation Épidémie prête à être déclenchée"})

    # POST /api/evacuation/epidemie/
    @action(detail=False, methods=["post"])
    def epidemie(self, request):
        e = Epidemie()
        e.evacuer()
        return Response({"status": "Évacuation Épidémie déclenchée"})

    # GET /api/evacuation/incendie/
    @action(detail=False, methods=["get"])
    def incendie(self, request):
        return Response({"message": "Évacuation Incendie prête à être déclenchée"})

    # POST /api/evacuation/incendie/
    @action(detail=False, methods=["post"])
    def incendie(self, request):
        i = Incendie()
        i.evacuer()
        return Response({"status": "Évacuation Incendie déclenchée"})

    # GET /api/evacuation/innondation/
    @action(detail=False, methods=["get"])
    def innondation(self, request):
        return Response({"message": "Évacuation Inondation prête à être déclenchée"})

    # POST /api/evacuation/innondation/
    @action(detail=False, methods=["post"])
    def innondation(self, request):
        n = Innondation()
        n.evacuer()
        return Response({"status": "Évacuation Inondation déclenchée"})

    # GET /api/evacuation/securite/
    @action(detail=False, methods=["get"])
    def securite(self, request):
        return Response({"message": "Évacuation Sécurité prête à être déclenchée"})

    # POST /api/evacuation/securite/
    @action(detail=False, methods=["post"])
    def securite(self, request):
        s = Securite()
        s.evacuer()
        return Response({"status": "Évacuation Sécurité déclenchée"})

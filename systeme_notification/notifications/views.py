from datetime import timedelta
import json

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notification


User = get_user_model()

def health(request):
    return HttpResponse("ok", content_type="text/plain")


@login_required
def user_dashboard(request):
    user = request.user
    notifications = (
        Notification.objects
        .filter(destinataire=user)
        .order_by("-created_at")
    )
    now = timezone.now()

    context = {
        "user": user,
        "notifications": notifications,
        "total_notifications": notifications.count(),
        "unread_notifications": notifications.filter(
            created_at__gte=now - timedelta(days=1)
        ).count(),
        "high_priority": notifications.filter(priority="haute").count(),
    }
    return render(request, "notifications/user_dashboard.html", context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    now = timezone.now()

    total_users = User.objects.count()
    total_notifications = Notification.objects.count()

    priority_stats = list(
        Notification.objects
        .values("priority")
        .annotate(count=Count("id"))
    )

    notifs_24h = Notification.objects.filter(
        created_at__gte=now - timedelta(hours=24)
    ).count()
    notifs_7d = Notification.objects.filter(
        created_at__gte=now - timedelta(days=7)
    ).count()
    notifs_30d = Notification.objects.filter(
        created_at__gte=now - timedelta(days=30)
    ).count()

    top_users = (
        User.objects
        .annotate(notif_count=Count("notification"))
        .order_by("-notif_count")[:5]
    )

    recent_notifications = (
        Notification.objects
        .all()
        .order_by("-created_at")[:10]
    )

    # Statistiques journalières sur 7 jours
    daily_stats = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = Notification.objects.filter(
            created_at__gte=day_start,
            created_at__lt=day_end,
        ).count()
        daily_stats.append(
            {"date": day_start.strftime("%d/%m"), "count": count}
        )
    daily_stats.reverse()

    context = {
        "total_users": total_users,
        "total_notifications": total_notifications,
        "priority_stats": priority_stats,
        "notifs_24h": notifs_24h,
        "notifs_7d": notifs_7d,
        "notifs_30d": notifs_30d,
        "top_users": top_users,
        "recent_notifications": recent_notifications,
        "daily_stats": json.dumps(daily_stats),
    }
    return render(request, "notifications/admin_dashboard.html", context)


@api_view(["GET"])
def stats_api(request):
    now = timezone.now()
    stats = {
        "total_users": User.objects.count(),
        "total_notifications": Notification.objects.count(),
        "notifs_24h": Notification.objects.filter(
            created_at__gte=now - timedelta(hours=24)
        ).count(),
        "notifs_7d": Notification.objects.filter(
            created_at__gte=now - timedelta(days=7)
        ).count(),
        "priority_counts": {
            "haute": Notification.objects.filter(priority="haute").count(),
            "moyenne": Notification.objects.filter(priority="moyenne").count(),
            "faible": Notification.objects.filter(priority="faible").count(),
        },
    }
    return Response(stats)


# URL de base de l’API d’évacuation :
# à configurer proprement dans settings.py, par exemple :
# EVACUATION_API_BASE = "https://security-campus.up.railway.app/api/evacuation/"
API_BASE = getattr(settings, "EVACUATION_API_BASE", "").rstrip("/")


class CustomLoginView(LoginView):
    template_name = "notifications/login.html"

    def get_success_url(self):
        user = self.request.user
        return "/dashboard/admin/" if user.is_superuser else "/dashboard/"


@login_required
@user_passes_test(lambda u: u.is_superuser)
def broadcast_notifications(request):
    if request.method == "POST":
        emergency_type = request.POST.get("emergency_type")

        if not API_BASE:
            messages.error(
                request,
                "Configuration API manquante (EVACUATION_API_BASE).",
            )
            return redirect("broadcast_notifications")

        endpoint_map = {
            "epidemie": f"{API_BASE}/epidemie/",
            "incendie": f"{API_BASE}/incendie/",
            "innondation": f"{API_BASE}/innondation/",
            "securite": f"{API_BASE}/securite/",
        }

        url = endpoint_map.get(emergency_type)

        if url:
            try:
                response = requests.post(url, timeout=5)
                if response.status_code == 200:
                    messages.success(
                        request, "Notification envoyée avec succès."
                    )
                else:
                    messages.error(
                        request,
                        f"Erreur API ({response.status_code})",
                    )
            except Exception as e:
                messages.error(request, f"Erreur API : {e}")
        else:
            messages.error(request, "Type d'urgence inconnu.")

        return redirect("broadcast_notifications")

    return render(request, "notifications/broadcast_notifications.html")

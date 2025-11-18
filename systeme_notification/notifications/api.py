from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
from rest_framework.renderers import OpenAPIRenderer, JSONOpenAPIRenderer

from django.db import transaction

from .models import Notification, User
from .serializers import NotificationSerializer
from .core import Epidemie, Incendie, Innondation, Securite

schema_view = get_schema_view(
    title="Campus Notification API",
    description="API pour gérer les notifications et déclencher des évacuations d'urgence",
    version="1.0.0",
    renderer_classes=[OpenAPIRenderer, JSONOpenAPIRenderer],
)

# ViewSet pour les notifications
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# APIViews pour les urgences
class EpidemieAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Épidémie prête à être déclenchée"})

    def post(self, request):
        e = Epidemie()
        # Exécuter la logique de l'urgence (activation alarme, haut‑parleur, etc.)
        e.evacuer()
        # Déterminer la priorité demandée ou utiliser « haute » par défaut
        level = request.data.get('level', 'haute').strip().lower()
        if not level:
            level = 'haute'
        # Message spécifique pour ce type d'urgence
        message = "Portez un masque"
        notifications = []
        # Utiliser une transaction pour assurer l'intégrité des écritures
        with transaction.atomic():
            for user in User.objects.filter(is_superuser=False):
                notifications.append(Notification(destinataire=user, message=message, priority=level))
            Notification.objects.bulk_create(notifications)
        return Response({"status": "Évacuation Épidémie déclenchée"})


class IncendieAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Incendie prête à être déclenchée"})

    def post(self, request):
        i = Incendie()
        i.evacuer()
        level = request.data.get('level', 'haute').strip().lower()
        if not level:
            level = 'haute'
        message = "Evacuez immédiatement"
        notifications = []
        with transaction.atomic():
            for user in User.objects.filter(is_superuser=False):
                notifications.append(Notification(destinataire=user, message=message, priority=level))
            Notification.objects.bulk_create(notifications)
        return Response({"status": "Évacuation Incendie déclenchée"})


class InnondationAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Innondation prête à être déclenchée"})

    def post(self, request):
        n = Innondation()
        n.evacuer()
        level = request.data.get('level', 'haute').strip().lower()
        if not level:
            level = 'haute'
        message = "Montez à l'étage"
        notifications = []
        with transaction.atomic():
            for user in User.objects.filter(is_superuser=False):
                notifications.append(Notification(destinataire=user, message=message, priority=level))
            Notification.objects.bulk_create(notifications)
        return Response({"status": "Évacuation Inondation déclenchée"})


class SecuriteAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Sécurité prête à être déclenchée"})

    def post(self, request):
        s = Securite()
        s.evacuer()
        level = request.data.get('level', 'haute').strip().lower()
        if not level:
            level = 'haute'
        message = "Suivez les consignes de sécurité"
        notifications = []
        with transaction.atomic():
            for user in User.objects.filter(is_superuser=False):
                notifications.append(Notification(destinataire=user, message=message, priority=level))
            Notification.objects.bulk_create(notifications)
        return Response({"status": "Évacuation Sécurité déclenchée"})

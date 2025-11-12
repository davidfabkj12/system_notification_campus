from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .core import Epidemie, Incendie, Innondation, Securite

# ------------------------------
# ViewSet pour les notifications
# ------------------------------
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# ------------------------------
# APIViews pour les urgences
# ------------------------------
class EpidemieAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Épidémie prête à être déclenchée"})

    def post(self, request):
        e = Epidemie()
        e.evacuer()
        return Response({"status": "Évacuation Épidémie déclenchée"})


class IncendieAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Incendie prête à être déclenchée"})

    def post(self, request):
        i = Incendie()
        i.evacuer()
        return Response({"status": "Évacuation Incendie déclenchée"})


class InnondationAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Innondation prête à être déclenchée"})

    def post(self, request):
        n = Innondation()
        n.evacuer()
        return Response({"status": "Évacuation Innondation déclenchée"})


class SecuriteAPIView(APIView):
    def get(self, request):
        return Response({"message": "Évacuation Sécurité prête à être déclenchée"})

    def post(self, request):
        s = Securite()
        s.evacuer()
        return Response({"status": "Évacuation Sécurité déclenchée"})

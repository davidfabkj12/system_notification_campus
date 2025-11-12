from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import NotificationViewSet, EpidemieAPIView, IncendieAPIView, InnondationAPIView, SecuriteAPIView

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('evacuation/epidemie/', EpidemieAPIView.as_view()),
    path('evacuation/incendie/', IncendieAPIView.as_view()),
    path('evacuation/innondation/', InnondationAPIView.as_view()),
    path('evacuation/securite/', SecuriteAPIView.as_view()),
]


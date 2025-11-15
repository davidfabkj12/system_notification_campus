from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
<<<<<<< Updated upstream
from .api import NotificationViewSet, EpidemieAPIView, IncendieAPIView, InnondationAPIView, SecuriteAPIView
=======
from .api import (
    NotificationViewSet,
    EpidemieAPIView,
    IncendieAPIView,
    InnondationAPIView,
    SecuriteAPIView,
)
from .views import (
    user_dashboard,
    admin_dashboard,
    stats_api,
    CustomLoginView,
    broadcast_notifications,
)
>>>>>>> Stashed changes

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
<<<<<<< Updated upstream
    path('', include(router.urls)),
    path('evacuation/epidemie/', EpidemieAPIView.as_view()),
    path('evacuation/incendie/', IncendieAPIView.as_view()),
    path('evacuation/innondation/', InnondationAPIView.as_view()),
    path('evacuation/securite/', SecuriteAPIView.as_view()),
=======
    # Page d'accueil : redirige vers le tableau de bord utilisateur
    path('', lambda request: redirect('dashboard/'), name='home'),
    # Authentification
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Dashboards
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),

    # Envoi de notifications à tous les utilisateurs (admin uniquement)
    path('dashboard/admin/broadcast/', broadcast_notifications, name='broadcast_notifications'),
    
    # API
    path('api/', include(router.urls)),
    path('api/stats/', stats_api, name='stats_api'),
    path('api/evacuation/epidemie/', EpidemieAPIView.as_view()),
    path('api/evacuation/incendie/', IncendieAPIView.as_view()),
    path('api/evacuation/innondation/', InnondationAPIView.as_view()),
    path('api/evacuation/securite/', SecuriteAPIView.as_view()),
>>>>>>> Stashed changes
]


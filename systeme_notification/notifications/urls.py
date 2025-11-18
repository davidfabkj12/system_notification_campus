from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

from .api import (
    NotificationViewSet,
    EpidemieAPIView,
    IncendieAPIView,
    InnondationAPIView,
    SecuriteAPIView,
    schema_view,
)
from .views import (
    user_dashboard,
    admin_dashboard,
    stats_api,
    CustomLoginView,
    broadcast_notifications,
)

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', lambda request: redirect('dashboard/'), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),


    # Dashboards
    path('dashboard/', user_dashboard, name='dashboard'),
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/broadcast/', broadcast_notifications, name='broadcast_notifications'),

    # API routes
    path('api/', include(router.urls)),
    path('api/stats/', stats_api, name='stats_api'),
    path('api/evacuation/epidemie/', EpidemieAPIView.as_view()),
    path('api/evacuation/incendie/', IncendieAPIView.as_view()),
    path('api/evacuation/innondation/', InnondationAPIView.as_view()),
    path('api/evacuation/securite/', SecuriteAPIView.as_view()),
    
    # OpenAPI schema
    path('api/schema/', schema_view, name='api-schema'),
]
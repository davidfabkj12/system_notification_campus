from django.contrib import admin
from django.urls import path, include
from notifications.views import health

urlpatterns = [
    path("", health, name="health"),
    path('admin/', admin.site.urls),
    path('', include('notifications.urls')),
]

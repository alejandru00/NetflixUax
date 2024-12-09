from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  # Rutas de autenticación
    path('', include('streaming.urls')),  # Rutas de streaming (home, series, películas)
]

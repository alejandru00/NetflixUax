from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('streaming.urls')),  # Incluye las rutas de la app streaming
    path('auth/', include('authentication.urls')),  # Incluye las rutas de la app authentication
]

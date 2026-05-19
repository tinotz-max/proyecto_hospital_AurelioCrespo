from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inventario/', include('inventario.urls')), # Agregamos esta línea
    path('', RedirectView.as_view(url='/inventario/dashboard/', permanent=False)),# Cambiamos la redirección
    path('usuarios/', include('usuarios.urls')),
]
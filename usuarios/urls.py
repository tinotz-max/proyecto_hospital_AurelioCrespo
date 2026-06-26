from django.urls import path
from . import views

urlpatterns = [
    path('supervisores/', views.lista_supervisores, name='lista_supervisores'),
    path('supervisores/nuevo/', views.crear_supervisor, name='crear_supervisor'),
    path('supervisores/editar/<int:pk>/', views.editar_supervisor, name='editar_supervisor'),
    path('supervisores/eliminar/<int:pk>/', views.eliminar_supervisor, name='eliminar_supervisor'),
]
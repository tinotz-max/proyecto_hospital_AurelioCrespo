from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('productos/', views.lista_productos, name='lista_productos'), 
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('lotes/nuevo/', views.crear_lote, name='crear_lote'),
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    # URLs para el ABML de Huecos
    path('huecos/', views.lista_huecos, name='lista_huecos'),
    path('huecos/nuevo/', views.crear_hueco, name='crear_hueco'),
    path('huecos/editar/<int:pk>/', views.editar_hueco, name='editar_hueco'),
    path('huecos/eliminar/<int:pk>/', views.eliminar_hueco, name='eliminar_hueco'),
    path('huecos/retiro/<int:hueco_id>/', views.registrar_retiro, name='registrar_retiro'),
    path('huecos/historial/', views.ver_historial_movimientos, name='ver_historial_movimientos'),
    path('lote/editar/<int:pk>/', views.editar_lote, name='editar_lote'),
    path('lote/eliminar/<int:pk>/', views.eliminar_lote, name='eliminar_lote'),
]
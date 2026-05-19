from django.contrib import admin
from .models import Laboratorio, Producto, Lote, Movimiento

admin.site.register(Laboratorio)
admin.site.register(Producto)
admin.site.register(Lote)
admin.site.register(Movimiento)
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# ==========================================
# 1. MODELOS DE BASE (Laboratorio y Producto)
# ==========================================

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    cod_barra = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    TIPO_CHOICES = [('MED', 'Medicamento'), ('DES', 'Descartable')]
    nombre = models.CharField(max_length=100)
    tipo_producto = models.CharField(max_length=50, choices=TIPO_CHOICES)
    refrigeracion = models.BooleanField(default=False)
    nivel_riesgo = models.CharField(max_length=50, blank=True)
    codigo_ocasa = models.CharField(max_length=50, unique=True)
    procedencia = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre


# ==========================================
# 2. NUEVO SISTEMA LOGÍSTICO (Departamentos y Huecos de Acceso Rápido)
# ==========================================

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Departamento")
    piso_ubicacion = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ubicación/Piso")

    def __str__(self):
        return self.nombre


class Hueco(models.Model):
    ESTADOS = [
        ('DISPONIBLE', 'Con Stock'),
        ('CRITICO', 'Stock Crítico'),
        ('VACIO', 'Sin Stock'),
    ]
    
    codigo_identificador = models.CharField(max_length=50, unique=True, verbose_name="Código de Hueco/Botiquín", default="PROV-000")
    insumo_nombre = models.CharField(max_length=100, verbose_name="Medicamento / Insumo", default="Insumo Genérico")
    cantidad_actual = models.PositiveIntegerField(default=0, verbose_name="Cantidad Disponible")
    capacidad_maxima = models.PositiveIntegerField(verbose_name="Capacidad Máxima de Almacenaje", default=100)
    
    # Al poner null=True y blank=True, Django permite crear la columna sin exigir un Departamento cargado de antemano
    departamento_asignado = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name="huecos", verbose_name="Departamento Destino", null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')

    def __str__(self):
        return f"{self.codigo_identificador} - {self.insumo_nombre}"


# ==========================================
# 3. GESTIÓN DE STOCK (Lotes y Movimientos Generales)
# ==========================================

class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    nro_lote = models.CharField(max_length=50)
    cantidad_actual = models.PositiveIntegerField(default=0)
    vencimiento = models.DateField()
    
    # Enlace limpio al nuevo modelo de Hueco provisional
    hueco = models.ForeignKey('Hueco', on_delete=models.SET_NULL, null=True, blank=True, related_name="lotes", verbose_name="Hueco Asignado")
    
    nro_deposito = models.IntegerField()
    sector = models.CharField(max_length=100)
    qr_data = models.TextField(blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - Lote: {self.nro_lote}"


class Movimiento(models.Model):
    TIPOS_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('BAJA', 'Baja/Vencimiento'),
    ]
    lote = models.ForeignKey(Lote, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=TIPOS_MOVIMIENTO)
    cantidad = models.IntegerField()
    motivo = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.lote.producto.nombre}"


# ==========================================
# 4. HISTORIAL DE MOVIMIENTOS REQUERIDO
# ==========================================

class HistorialRetiro(models.Model):
    """
    Tabla principal para construir el historial detallado de movimientos de acceso rápido.
    """
    hueco = models.ForeignKey(Hueco, on_delete=models.SET_NULL, null=True, related_name="retiros", verbose_name="Hueco de Origen")
    insumo_retirado = models.CharField(max_length=100, verbose_name="Insumo Extraído")
    departamento_destino = models.ForeignKey(Departamento, on_delete=models.CASCADE, verbose_name="Departamento/Uso Destinado")
    ubicacion_en_retiro = models.CharField(max_length=150, verbose_name="Ubicación exacta al momento del retiro")
    cantidad_retirada = models.PositiveIntegerField(verbose_name="Cantidad Retirada")
    fecha_retiro = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora del Retiro")
    usuario_supervisor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Supervisor Responsable")

    def __str__(self):
        return f"Retiro {self.cantidad_retirada}x {self.insumo_retirado} -> {self.departamento_destino.nombre} ({self.fecha_retiro.strftime('%d/%m/%Y %H:%M')})"
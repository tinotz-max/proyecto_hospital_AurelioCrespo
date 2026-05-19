from django.db import models
from django.contrib.auth.models import User

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

# 🆕 AGREGAMOS ESTA CLASE PARA TU ABML DE HUECOS
class Hueco(models.Model):
    ESTADOS = [('LIBRE', 'Libre'), ('OCUPADO', 'Ocupado')]
    
    codigo = models.CharField(max_length=50, unique=True) # Ej: "Estante-A1"
    nro_deposito = models.IntegerField()
    sector = models.CharField(max_length=100)
    estado = models.CharField(max_length=15, choices=ESTADOS, default='LIBRE')

    def __str__(self):
        return f"Hueco {self.codigo} ({self.sector})"

class Lote(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='lotes')
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.SET_NULL, null=True, blank=True)
    nro_lote = models.CharField(max_length=50)
    cantidad_actual = models.PositiveIntegerField(default=0)
    vencimiento = models.DateField()
    
    # 🔗 Conectamos el Lote al Hueco. Usamos models.PROTECT para cumplir tu Caso de Prueba:
    # Si el hueco tiene un lote adentro, Django NO va a dejar que borren el hueco.
    hueco = models.ForeignKey(Hueco, on_delete=models.PROTECT, null=True, blank=True, related_name='lotes')
    
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
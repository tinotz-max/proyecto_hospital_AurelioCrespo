from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Producto, Lote
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import Hueco
from .forms import HuecoForm


@login_required # Esto asegura que si no estás logueado, te mande al login
def dashboard(request):
    # Por ahora solo contaremos cuántos productos y lotes hay
    total_productos = Producto.objects.count()
    total_lotes = Lote.objects.count()
    
    context = {
        'total_productos': total_productos,
        'total_lotes': total_lotes,
    }
    return render(request, 'inventario/dashboard.html', context)
# Create your views here.
from .models import Producto  # Asegúrate de tener la importación

@login_required
def lista_productos(request):
    # Obtenemos todos los productos
    productos = Producto.objects.all()
    
    return render(request, 'inventario/lista_productos.html', {'productos': productos})

from .forms import ProductoForm

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos') # Al guardar, volvemos a la tabla
    else:
        form = ProductoForm()
    
    return render(request, 'inventario/form_producto.html', {'form': form})

from .models import Lote
from .forms import LoteForm

@login_required
def crear_lote(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = LoteForm()
    return render(request, 'inventario/form_lote.html', {'form': form})
 

@login_required
def lista_lotes(request):
    # Traemos los lotes, ordenados por los que vencen más pronto
    lotes = Lote.objects.all().order_by('vencimiento')
    return render(request, 'inventario/lista_lotes.html', {'lotes': lotes})

# 1. LECTURA: Listar todos los huecos
@login_required
def lista_huecos(request):
    huecos = Hueco.objects.all()
    return render(request, 'inventario/lista_huecos.html', {'huecos': huecos})

# 2. ALTA: Crear un nuevo hueco
@login_required
def crear_hueco(request):
    if request.method == 'POST':
        form = HuecoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hueco creado con éxito.")
            return redirect('lista_huecos')
    else:
        form = HuecoForm()
    return render(request, 'inventario/form_hueco.html', {'form': form, 'titulo': 'Nuevo Hueco'})

# 3. MODIFICACIÓN: Editar un hueco existente
@login_required
def editar_hueco(request, pk):
    hueco = get_object_or_404(Hueco, pk=pk)
    if request.method == 'POST':
        form = HuecoForm(request.POST, instance=hueco)
        if form.is_valid():
            form.save()
            messages.success(request, "Hueco actualizado con éxito.")
            return redirect('lista_huecos')
    else:
        form = HuecoForm(instance=hueco)
    return render(request, 'inventario/form_hueco.html', {'form': form, 'titulo': 'Editar Hueco'})

# 4. BAJA: Eliminar un hueco (Con protección si tiene stock)
@login_required
def eliminar_hueco(request, pk):
    hueco = get_object_or_404(Hueco, pk=pk)
    try:
        hueco.delete()
        messages.success(request, "Hueco eliminado correctamente.")
    except Exception:
        # Aquí actúa el models.PROTECT de la base de datos si hay medicamentos asociados
        messages.error(request, "No se puede eliminar: Este hueco contiene lotes activos de medicamentos.")
    return redirect('lista_huecos')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Hueco, Producto, Lote
from usuarios.models import Perfil # Importamos Perfil para contar supervisores

@login_required
def dashboard(request):
    # Contamos los datos reales de la base de datos
    context = {
        'total_huecos': Hueco.objects.count(),
        'huecos_libres': Hueco.objects.filter(estado='LIBRE').count(),
        'total_supervisores': Perfil.objects.filter(rol='SUPERVISOR').count(),
        'total_productos': Producto.objects.count(),
        'total_lotes': Lote.objects.count(),
    }
    return render(request, 'inventario/dashboard.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Hueco, HistorialRetiro, Departamento

@login_required
def registrar_retiro(request, hueco_id):
    hueco = get_object_or_404(Hueco, id=hueco_id)
    departamentos = Departamento.objects.all()
    
    if request.method == 'POST':
        id_dep_destino = request.POST.get('departamento_destino')
        cantidad = int(request.POST.get('cantidad_retirada'))
        dep_destino = get_object_or_404(Departamento, id=id_dep_destino)
        
        # Validación crítica: ¿Hay stock suficiente en este almacén provisional?
        if cantidad > hueco.cantidad_actual:
            messages.error(request, f"Error: No podés retirar {cantidad} unidades. El hueco solo tiene {hueco.cantidad_actual} disponibles.")
            return render(request, 'inventario/registrar_retiro.html', {'hueco': hueco, 'departamentos': departamentos})
        
        # 1. Restamos el stock del hueco
        hueco.cantidad_actual -= cantidad
        if hueco.cantidad_actual == 0:
            hueco.estado = 'VACIO'
        elif hueco.cantidad_actual < (hueco.capacidad_maxima * 0.2): # menos del 20%
            hueco.estado = 'CRITICO'
        hueco.save()
        
        # 2. Creamos la línea en el historial detallado de movimientos
        HistorialRetiro.objects.create(
            hueco=hueco,
            insumo_retirado=hueco.insumo_nombre,
            departamento_destino=dep_destino,
            ubicacion_en_retiro=f"Piso: {dep_destino.piso_ubicacion} - Sector: {dep_destino.nombre}",
            cantidad_retirada=cantidad,
            usuario_supervisor=request.user # El usuario logueado en Brave
        )
        
        messages.success(request, f"Retiro de {cantidad} {hueco.insumo_nombre} asentado en el historial con éxito.")
        return redirect('lista_huecos') # O la vista de tu dashboard

    return render(request, 'inventario/form_retiro.html', {'hueco': hueco, 'departamentos': departamentos})


@login_required
def ver_historial_movimientos(request):
    """Vista para renderizar la tabla del historial general exigido"""
    movimientos = HistorialRetiro.objects.all().order_by('-fecha_retiro')
    return render(request, 'inventario/historial.html', {'movimientos': movimientos})
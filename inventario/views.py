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
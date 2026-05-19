from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Perfil
from .forms import SupervisorForm
from django.shortcuts import get_object_or_404
from django.contrib import messages


def lista_supervisores(request):
    # Traemos todos los perfiles que tienen rol de SUPERVISOR
    supervisores = Perfil.objects.filter(rol='SUPERVISOR')
    return render(request, 'usuarios/lista_supervisores.html', {'supervisores': supervisores})

def crear_supervisor(request):
    if request.method == 'POST':
        form = SupervisorForm(request.POST)
        if form.is_valid():
            # 1. Creamos el usuario de Django
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )
            # 2. Creamos el perfil asociado
            perfil = form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect('lista_supervisores')
    else:
        form = SupervisorForm()
    return render(request, 'usuarios/form_supervisor.html', {'form': form})
# MODIFICACIÓN de Supervisor
def editar_supervisor(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        form = SupervisorForm(request.POST, instance=perfil)
        if form.is_valid():
            # Actualizamos el email del usuario de Django asociado
            perfil.user.email = form.cleaned_data['email']
            perfil.user.save()
            form.save()
            messages.success(request, "Datos del supervisor actualizados.")
            return redirect('lista_supervisores')
    else:
        # Cargamos el form con los datos actuales
        initial_data = {'username': perfil.user.username, 'email': perfil.user.email}
        form = SupervisorForm(instance=perfil, initial=initial_data)
        # Bloqueamos el username porque no debería cambiarse
        form.fields['username'].widget.attrs['readonly'] = True 
        
    return render(request, 'usuarios/form_supervisor.html', {'form': form, 'editando': True})

# BAJA de Supervisor
def eliminar_supervisor(request, pk):
    perfil = get_object_or_404(Perfil, pk=pk)
    user = perfil.user
    user.delete() # Al borrar el User, se borra el Perfil automáticamente (CASCADE)
    messages.success(request, "Supervisor eliminado del sistema.")
    return redirect('lista_supervisores')
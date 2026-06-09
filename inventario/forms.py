from django import forms
from .models import Producto
from .models import Hueco

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Elegimos los campos que el usuario va a llenar
        fields = ['nombre', 'tipo_producto', 'refrigeracion', 'nivel_riesgo', 'codigo_ocasa', 'procedencia']
        
        # Le agregamos clases de Bootstrap a los inputs para que se vean bien
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Paracetamol 500mg'}),
            'tipo_producto': forms.Select(attrs={'class': 'form-select'}),
            'nivel_riesgo': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_ocasa': forms.TextInput(attrs={'class': 'form-control'}),
            'procedencia': forms.TextInput(attrs={'class': 'form-control'}),
            'refrigeracion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
from .models import Lote 

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['producto', 'laboratorio', 'nro_lote', 'cantidad_actual', 'vencimiento', 'nro_deposito', 'sector']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'laboratorio': forms.Select(attrs={'class': 'form-select'}),
            'nro_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), # Calendario
            'nro_deposito': forms.NumberInput(attrs={'class': 'form-control'}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Hueco, HistorialRetiro

class HuecoForm(forms.ModelForm):
    class Meta:
        model = Hueco
        # Incluimos los campos nuevos que definimos en el modelo
        fields = [
            'codigo_identificador', 
            'insumo_nombre', 
            'cantidad_actual', 
            'capacidad_maxima', 
            'departamento_asignado',
            'estado'
        ]
        widgets = {
            'codigo_identificador': forms.TextInput(attrs={'class': 'form-control'}),
            'insumo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'departamento_asignado': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

# Aprovechamos para crear el formulario del nuevo historial solicitado
class RetiroForm(forms.ModelForm):
    class Meta:
        model = HistorialRetiro
        fields = ['departamento_destino', 'cantidad_retirada']
        widgets = {
            'departamento_destino': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_retirada': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
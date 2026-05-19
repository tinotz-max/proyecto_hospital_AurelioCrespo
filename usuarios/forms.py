from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class SupervisorForm(forms.ModelForm):
    # Campos adicionales para el Usuario de Django
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Perfil
        fields = ['legajo', 'rol']
        widgets = {
            'legajo': forms.TextInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }
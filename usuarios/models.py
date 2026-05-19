from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES_CHOICES = [
        ('AGENTE', 'Agente de Stock'),
        ('SUPERVISOR', 'Supervisor del Hospital'),
    ]
    
    # Esto une de forma única el usuario de Django con nuestro perfil de roles
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='AGENTE')
    legajo = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
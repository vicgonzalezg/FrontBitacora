from django.db import models

# Create your models here.

class User(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    contraseña = models.CharField(max_length=50)

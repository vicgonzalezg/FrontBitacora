from django.db import models
from datetime import datetime,timedelta

# Create your models here.

class User(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(blank=True)
    contraseña = models.CharField(max_length=50)


#Ordenar de A-Z

class Archivo(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    ARCHIVO = models.CharField(max_length=4000,blank=True, null=True)
    LINK = models.CharField(max_length=4000, blank=True, null=True)
    SESION_ID = models.BigIntegerField()
    TIPOARCHIVO_ID = models.BigIntegerField()

class Enlace(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    LINK = models.CharField(max_length=4000, blank=True, null=True)
    SESION_ID = models.BigIntegerField()


class EstadoProceso(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    DESCRIPCION = models.CharField(max_length=100)
    ACTIVO = models.BigIntegerField()


class EstadoSesion(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    DESCRIPCION = models.CharField(max_length=100)
    ACTIVO = models.BigIntegerField()

class Perfil(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    NOMBRE = models.CharField(max_length=100)
    ACTIVO = models.BigIntegerField()


class Proceso(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    NOMBREEMPRESA = models.CharField(max_length=100)
    CANTSESIONES = models.BigIntegerField()
    OBJETIVOS = models.CharField(max_length=4000, blank=True, null=True)
    INDICADORES = models.CharField(max_length=4000, blank=True, null=True)
    PLANACCION = models.CharField(max_length=4000, blank=True, null=True)
    FECHACREACION = models.DateField()
    FECHATERMINO = models.DateField(blank=True, null=True)
    ACTIVO = models.BigIntegerField()
    ESTADOPROCESO_ID = models.BigIntegerField()
    ADMINISTRADOR_ID = models.BigIntegerField()
    COACH_ID = models.BigIntegerField()
    COACHEE_ID = models.BigIntegerField()


class Sesion(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    FECHASESION = models.DateField(blank=True, null=True)
    DESCRIPCION = models.CharField(max_length=4000, blank=True, null=True)
    AVANCES = models.CharField(max_length=4000, blank=True, null=True)
    ASIGNACION = models.CharField(max_length=4000, blank=True, null=True)
    ACTIVO = models.BigIntegerField()
    PROCESO_ID = models.BigIntegerField()
    ESTADOSESION_ID = models.BigIntegerField()


class TipoArchivo(models.Model):
    ID = models.BigIntegerField(primary_key=True)
    FORMATO = models.CharField(max_length=100)
    TAMANO = models.BigIntegerField()
    ACTIVO = models.BigIntegerField()

class Usuario(models.Model):
    ID = models.BigIntegerField(primary_key=True)#Tiene autoincrementable secuencial.
    USUARIO = models.CharField(max_length=100)
    CONTRASENA = models.CharField(max_length=400)
    NOMBRE = models.CharField(max_length=100)
    SNOMBRE = models.CharField(max_length=100, blank=True, null=True)
    APELLIDO = models.CharField(max_length=100)
    SAPELLIDO = models.CharField(max_length=100, blank=True, null=True)
    CORREO = models.CharField(max_length=100)
    FONO = models.CharField(max_length=100, blank=True, null=True)
    IDIOMA = models.CharField(max_length=50, blank=True, null=True)
    EMPRESA = models.CharField(max_length=100, blank=True, null=True)
    NOMBREJEFE = models.CharField(max_length=100, blank=True, null=True)
    EMAILJEFE = models.CharField(max_length=100, blank=True, null=True)
    FONOJEFE = models.CharField(max_length=100, blank=True, null=True)
    ACTIVO = models.BigIntegerField()
    PERFIL_ID = models.BigIntegerField()


        

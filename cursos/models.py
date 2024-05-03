from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Profesor(models.Model):
    rut = models.CharField(primary_key=True, max_length=9,null=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    activo = models.BooleanField(default=False)
    creacion_registro = models.DateField(auto_now_add=True)
    modificacion_registro = models.DateField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    cursos = models.ManyToManyField('Curso', through='CursoProfesor')

    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Curso(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10,null=False, unique=True)
    nombre = models.CharField(max_length=50)
    version = models.IntegerField()
    profesor_id = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    

    def __str__(self):
        return self.nombre
    
class CursoProfesor(models.Model):
    curso_id = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
    profesor_id = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    creacion_registro = models.DateField(auto_now_add=True)
    modificacion_registro = models.DateField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.curso_id + ' ' + self.profesor_id
    

class Estudiante(models.Model):
    rut = models.CharField(primary_key=True, max_length=9,null=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nac = models.DateField(null=False)
    activo = models.BooleanField(default=False)
    creacion_registro = models.DateField(auto_now_add=True)
    modificacion_registro = models.DateField(auto_now=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    curso_id = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Direccion(models.Model):
    calle = models.CharField(max_length=50,null=False)
    numero = models.CharField(max_length=10,null=False)
    depto = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50,null=False)
    ciudad = models.CharField(max_length=50, null=False)
    region = models.CharField(max_length=50, null=False)
    estudiante_id = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.calle + ' ' + self.numero


    

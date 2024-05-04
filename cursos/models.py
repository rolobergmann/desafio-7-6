from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
""" class User(AbstractUser):
    # ... your custom User model fields and customizations

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_groups', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField( 
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    ) """
class Profesor(models.Model):
    rut = models.CharField(primary_key=True, max_length=9,null=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    activo = models.BooleanField(default=False)
    creacion_registro = models.DateField(auto_now_add=True)
    modificacion_registro = models.DateField(auto_now=True)
    creado_por = models.CharField(max_length=50)

    cursos = models.ManyToManyField('Curso', through='CursoProfesor',related_name='profesores')

    def __str__(self):
        return self.nombre + ' ' + self.apellido + ' ' + self.rut
    
class Estudiante(models.Model):
    rut = models.CharField(primary_key=True, max_length=9,null=False)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    fecha_nac = models.DateField(null=False)
    activo = models.BooleanField(default=False)
    creacion_registro = models.DateField(auto_now_add=True)
    modificacion_registro = models.DateField(auto_now=True)
    creado_por = models.CharField(max_length=50)
    curso = models.ForeignKey('Curso', on_delete=models.DO_NOTHING, null=True, related_name='estudiantes')
    
    def __str__(self):
        return self.nombre + ' ' + self.apellido
    
class Curso(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10,null=False, unique=True)
    nombre = models.CharField(max_length=50)
    version = models.IntegerField()
    profesor_id = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING, null=True)
    

    def __str__(self):
        return self.nombre
class CursoProfesor(models.Model):
    curso_id = models.ForeignKey(Curso, on_delete=models.DO_NOTHING)
    profesor_id = models.ForeignKey(Profesor, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.curso_id + ' ' + self.profesor_id



class Direccion(models.Model):
    calle = models.CharField(max_length=50,null=False)
    numero = models.CharField(max_length=10,null=False)
    depto = models.CharField(max_length=50)
    comuna = models.CharField(max_length=50,null=False)
    ciudad = models.CharField(max_length=50, null=False)
    region = models.CharField(max_length=50, null=False)
    estudiante_id = models.OneToOneField(Estudiante, on_delete=models.DO_NOTHING, null=True)
    
    def __str__(self):
        return self.calle + ' ' + self.numero


    

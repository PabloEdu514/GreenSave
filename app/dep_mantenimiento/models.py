from django.db import models
from django.contrib.auth.models import User

class dep_mantenimiento(models.Model):
    user = models.IntegerField(User)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', blank=True, null= True)
    usuario_activo = models.BooleanField(default=True)
    carrera = models.CharField('Carrera', max_length = 200, blank=True, null= True)
    rol = models.CharField('Rol', max_length=40)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = u'userDep'


    
    
class solicitante(models.Model):
    id= models.IntegerField(primary_key=True) 
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    area= models.CharField(max_length=50)
    cargo= models.CharField(max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitante'
        
   
  ####  
class trabajadores(models.Model):
    id= models.IntegerField(primary_key=True) 
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    num_solicitudes=models.IntegerField()
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'trabajadores'

class jefDepartamento(models.Model):
    id= models.IntegerField(primary_key=True) 
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    departamento= models.CharField(max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'jefDepartamento'
    
class jefMantenimiento(models.Model):
    id= models.IntegerField(primary_key=True) 
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    trabajadores=models.ForeignKey(trabajadores, on_delete=models.CASCADE)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'jefMantenimiento'

class subdirectora(models.Model):
    id= models.IntegerField(primary_key=True) 
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'subdirectora'
    
class Solicitud(models.Model):
    id= models.IntegerField (primary_key=True)
    folio= models.IntegerField()
    area_solicitante= models.CharField(max_length=50)
    responsable_Area= models.CharField(max_length=50)
    servicos={
        ('Electrica','Electrica'),
        ('Herrería','Herrería'),
        ('Plomería','Plomería'),
        ('Pintura','Pintura'),
        ('Cañones','Cañones'),
        ('Pintarrón','Pintarrón'),
        ('Cerrajería','Cerrajería'),
        ('Otro','Otro')
        
    }
    
    tipo_servicio= models.CharField(choices=servicos,max_length=50)
    descripcion= models.CharField(max_length=50)
    des_Serv_Realizado= models.CharField(max_length=50)
    des_Serv_no_Realizado= models.CharField(max_length=50)
    estatus={
        ('Pendiente','Pendiente'),
        ('Realizada','Realizada'),
        ('Rechazada','Rechazada'),
        ('Cancelada','Cancelada'),
        ('En proceso','En proceso'),
        ('En espera','En espera')
        
    }
    
    status= models.CharField(choices=estatus,max_length=50)
    solicitante=models.ForeignKey(solicitante, on_delete=models.CASCADE)
    jefMantenimiento=models.ForeignKey(jefMantenimiento, on_delete=models.CASCADE)
    jefDepartamento=models.ForeignKey(jefDepartamento, on_delete=models.CASCADE)
    trabajadores=models.ForeignKey(trabajadores, on_delete=models.CASCADE)
    subdirectora=models.ForeignKey(subdirectora,null=True, on_delete=models.CASCADE)
    fecha= models.DateField()
    hora= models.TimeField()
    material_utilizado= models.CharField(null=True,max_length=50)
    imagen= models.FileField(null=True,upload_to='dep_mantenimiento/img')
    motv_rechazo= models.CharField(null=True,max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitudes'
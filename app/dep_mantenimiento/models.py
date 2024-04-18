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
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    num_solicitudes=models.IntegerField()
    puesto=models.CharField(max_length=50)# si es jefe, docente etc
    departamento=models.CharField(max_length=50)#y al departamento que pertenece 
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'trabajadores'

class jefDepartamento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    departamento= models.CharField(max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'jefDepartamento'
    
class jefMantenimiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'jefMantenimiento'
class jefMantenimiento_trabajadores(models.Model):
    jefmantenimiento = models.ForeignKey(jefMantenimiento, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(trabajadores, on_delete=models.CASCADE)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'JefeMantenimiento_trabajadores'
    
class subdirectora(models.Model):
    id = models.AutoField(primary_key=True)
    nombre= models.CharField(max_length=50)
    apellidosPaterno= models.CharField(max_length=50)
    apellidosMaterno= models.CharField(max_length=50)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'subdirectora'
    
class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    folio= models.IntegerField(null=False)
    area_solicitante= models.CharField(max_length=50,null=False)
    responsable_Area= models.CharField(max_length=50,null=False)
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
    
    tipo_servicio= models.CharField(choices=servicos,max_length=50,null=False)
    descripcion= models.CharField(max_length=3000,null=False)
    des_Serv_Realizado= models.CharField(max_length=3000,null=True)
    des_Serv_no_Realizado= models.CharField(max_length=3000,null=True)
    estatus={
        ('Pendiente','Pendiente'),
        ('Realizada','Realizada'),
        ('Rechazada','Rechazada'),
        ('Cancelada','Cancelada'),
        ('En proceso','En proceso'),
        ('En espera','En espera')
        
    }
    
    status= models.CharField(choices=estatus,max_length=50)
    solicitante=models.ForeignKey(solicitante, on_delete=models.CASCADE,null=True)
    jefMantenimiento=models.ForeignKey(jefMantenimiento, on_delete=models.CASCADE,null=True)
    jefDepartamento=models.ForeignKey(jefDepartamento, on_delete=models.CASCADE,null=True)
    trabajadores=models.ForeignKey(trabajadores, on_delete=models.CASCADE,null=True)
    subdirectora=models.ForeignKey(subdirectora, on_delete=models.CASCADE,null=True)
    fecha= models.DateField(null=False)
    hora= models.TimeField(null=False)
    material_utilizado= models.CharField(null=True,max_length=3000)
    imagen= models.FileField(null=True,upload_to='dep_mantenimiento/img')
    motv_rechazo= models.CharField(null=True,max_length=3000)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitudes'
       
        
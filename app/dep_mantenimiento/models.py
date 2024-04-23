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


    
    
   

class trabajadores(models.Model):
    id = models.AutoField(primary_key=True)
    nombres= models.CharField(max_length=200)
    apPaterno= models.CharField(max_length=200)
    apMaterno= models.CharField(max_length=200)
    puesto=models.CharField(max_length=100)# si es jefe, docente etc
    departamento=models.CharField(max_length=100)#y al departamento que pertenece 
    email= models.CharField(max_length=200)
    campus= models.CharField(max_length=100)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'trabajadores'
class empleado(models.Model):
    id = models.AutoField(primary_key=True)
    nombres= models.CharField(max_length=200)
    apPaterno= models.CharField(max_length=200)
    apMaterno= models.CharField(max_length=200)
    email= models.CharField(max_length=200)
    SolComplidas=models.IntegerField()
    fecha= models.DateField()
    semestre= models.CharField(max_length=150)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'empleado'
    
class Solicitud(models.Model):
    id = models.AutoField(primary_key=True)
    folio= models.IntegerField(null=False)
    area_solicitante= models.CharField(max_length=150,null=False)
    responsable_Area= models.CharField(max_length=300,null=False)
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
    
    tipo_servicio= models.CharField(choices=servicos,max_length=100,null=False)
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
    fecha= models.DateField(null=False)
    hora= models.TimeField(null=False)
    material_asignado= models.CharField(null=True,max_length=3000)
    material_utilizado= models.CharField(null=True,max_length=3000)
    imagen= models.FileField(null=True,upload_to='dep_mantenimiento/img')
    motv_rechazo= models.CharField(null=True,max_length=3000)
   # Relaciones con los trabajadores
    id_Trabajador = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_trabajador', null=True)
    id_Jefe_Departamento = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_jefe_departamento', null=True)
    id_Jefe_Mantenimiento = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_jefe_mantenimiento', null=True)
    id_Subdirectora = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_subdirectora', null=True)
    id_Empleado = models.ForeignKey('empleado', on_delete=models.CASCADE, related_name='solicitudes_empleado', null=True)
    
    # Campos para firmas
    firma_Jefe_Departamento = models.BooleanField(default=False)
    firma_Empleado = models.BooleanField(default=False)
    firma_Jefe_Mantenimiento = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitudes'
       
        
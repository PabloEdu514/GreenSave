from django.utils import timezone

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
class trabajadores(models.Model):
    SEXO = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    )
    Activo = (
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    )

    Puestos={
        ('Subdirector','Subdirector/a'),
        ('Jefe','Jefe'),
        ('Docente','Docente'),
        ('Empleado','Empleado'),
        ('Secretario','Secretario/a')     
        
    }
    id=models.AutoField(primary_key=True)
    user_id=models.PositiveIntegerField( null=True, blank=True)
    nombres = models.CharField("Nombre(s)", max_length=40, db_column='nombres',blank=True, null=True)
    appaterno = models.CharField("Apellido Paterno", max_length=40, db_column='appaterno', blank=True, null=True)
    apmaterno = models.CharField("Apellido Materno", max_length=40, db_column='apmaterno', blank=True, null=True)
    activo = models.CharField(choices=Activo, max_length=15, db_column='activo', blank=True, null=True, default="activo")
    sexo = models.CharField("Sexo", max_length=1, choices=SEXO, db_column='sexo',blank=True, null=True)
    puesto=models.CharField(choices=Puestos,max_length=100,blank=True, null=True)# si es jefe, docente etc 
    departamento=models.CharField(max_length=100,blank=True, null=True)#y al departamento que pertenece 
    campus= models.PositiveIntegerField( null=True, blank=True)
    email = models.EmailField("Correo", max_length=100, db_column='email', blank=True, null=True)
    foto_Perfil = models.ImageField('Imagen de Perfil', upload_to='dep_mantenimiento/img/Foto_Perfil', blank=True, null= True)
    grupos = models.ManyToManyField('CustomGroup', related_name='trabajadores', blank=True)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'trabajador'
        verbose_name = 'Perfil de trabajador'
        permissions = [
        ('view_mantenimiento_trabajador', 'Usuarios de Mantenimiento de Equipo pueden ver'),
        ('change_mantenimiento_trabajador', 'Usuarios de Mantenimiento de Equipo pueden editar'),
        ('view_all_trabajador', 'Usuarios Solcitantes pueden ver'),
        ('change_all_trabajador', 'Usuarios Solcitantes pueden editar'),
        ('add_all_trabajador', 'Usuarios Solcitantes pueden agregar'),
        ('delete_all_trabajador', 'Usuarios Solcitantes pueden borrar')
        ]
        
    def nombre_completo(self):
        nombre= self.nombres+" "+self.appaterno+" "+self.apmaterno
        return nombre
    
    def __str__(self):
        return self.nombre_completo()
    
class Solicitud_Mantenimiento(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    folio= models.IntegerField(null=False,blank=True)
    area_solicitante= models.CharField(max_length=150,null=False,blank=True)
    responsable_Area= models.CharField(max_length=300,null=False,blank=True)
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
    
    tipo_servicio= models.CharField(choices=servicos,max_length=100,null=False,blank=True)
    descripcion= models.CharField(max_length=3000,null=False,blank=True)
    des_Serv_Realizado= models.CharField(max_length=3000,null=True,blank=True)
    des_Serv_no_Realizado= models.CharField(max_length=3000,null=True,blank=True)
    estatus={
        ('Enviado','Enviado'),
        ('Pendiente','Pendiente'),
        ('Realizado','Realizado'),
        ('Rechazado','Rechazado'),
        ('Alerta','Alerta'),
        ('En_proceso','En proceso'),
        ('En_espera','En espera')
        
    }
    
    status= models.CharField(choices=estatus,max_length=50,blank=True)
    fecha= models.DateField(null=False,blank=True)
    hora= models.TimeField(null=False,blank=True)

    material_asignado= models.CharField(null=True,max_length=3000,blank=True)
    material_utilizado= models.CharField(null=True,max_length=3000,blank=True)
    imagen= models.FileField(null=True,upload_to='dep_mantenimiento/img',blank=True)
    motv_rechazo= models.CharField(null=True,max_length=3000,blank=True)
   # Relaciones con los trabajadores
    id_Trabajador = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_trabajador', null=True,blank=True)
    id_Jefe_Departamento = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_jefe_departamento', null=True,blank=True)
    id_Jefe_Mantenimiento = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_jefe_mantenimiento', null=True,blank=True)
    id_Subdirectora = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_subdirectora', null=True,blank=True)
    id_Empleado = models.ForeignKey('trabajadores', on_delete=models.CASCADE, related_name='solicitudes_empleado', null=True,blank=True)
    
    # Campos para firmas
    firma_Jefe_Departamento = models.BooleanField(default=False,blank=True)
    firma_Empleado = models.BooleanField(default=False,blank=True)
    firma_Jefe_Mantenimiento = models.BooleanField(default=False,blank=True)
    resolvio = models.BooleanField(default=False,blank=True)
    # Imagenes de las firmas
    firma_Jefe_Departamento_img= models.ImageField(null=True,upload_to='dep_mantenimiento/img',blank=True)
    firma_Empleado_img= models.ImageField(null=True,upload_to='dep_mantenimiento/img',blank=True)
    firma_Jefe_Mantenimiento_img= models.ImageField(null=True,upload_to='dep_mantenimiento/img',blank=True)
    
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitud_mantenimiento'
        verbose_name = 'Solicitud_de_mantenimiento'
        permissions = [
            #Permisos para Solicitante
            ('view_Solicitud_Mantenimiento_Solicitantes', 'Usuarios Solicitantes pueden ver las solicitudes de mantenimiento'),
            ('change_Solicitud_Mantenimiento_Solicitantes', 'Usuarios Solicitantes pueden cambiar las solicitudes de mantenimiento'),
            ('add_Solicitud_Mantenimiento_Solicitantes', 'Usuarios Solicitantes pueden agregar las solicitudes de mantenimiento'),
            ('delete_Solicitud_Mantenimiento_Solicitantes', 'Usuarios Solicitantes pueden borrar las solicitudes de mantenimiento'),
            
            #Permisos para Mantenimiento
            ('view_Solicitud_Mantenimiento_Mantenimiento', 'Usuarios Mantenimiento pueden ver las solicitudes de mantenimiento'),
            ('change_Solicitud_Mantenimiento_Mantenimiento', 'Usuarios Mantenimiento pueden cambiar las solicitudes de mantenimiento'),
        ]# Modelo para los grupos personalizados
        
class HistorialSolicitud(models.Model):
    solicitud = models.ForeignKey('Solicitud_Mantenimiento', on_delete=models.CASCADE, related_name='historial')
    fecha_hora = models.DateTimeField(default=timezone.now)
    nuevo_status = models.CharField(choices=Solicitud_Mantenimiento.estatus, max_length=50)

    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'historial_solicitud'
        verbose_name = 'Historial de Solicitud'        
        
        
class CustomGroup(models.Model):
    name = models.CharField(max_length=150, unique=True)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'Grupos'
        verbose_name = 'Grupo'
    def __str__(self):
        return self.name

# Define tus señales aquí
@receiver(post_save, sender=trabajadores)
def asignar_grupo(sender, instance, created, **kwargs):
    if created:
        if instance.puesto == 'Jefe' or instance.puesto == 'Empleado' and  instance.departamento == 'Mantenimiento de Equipo':
           
                grupo, _ = CustomGroup.objects.get_or_create(name='Trabajadores de Mantenimiento')
                instance.grupos.add(grupo)
        else:
            grupo, _ = CustomGroup.objects.get_or_create(name='Usuarios Solicitantes')
            instance.grupos.add(grupo)
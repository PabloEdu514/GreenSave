from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

class trabajadores(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.PositiveIntegerField( null=True, blank=True)
    Puestos={
        ('Subdirector','Subdirector/a'),
        ('Jefe','Jefe'),
        ('Docente','Docente'),
        ('Empleado','Empleado'),
        ('Secretario','Secretario/a')
       
        
    }
    puesto=models.CharField(choices=Puestos,max_length=100,blank=True)# si es jefe, docente etc
    departamento=models.CharField(max_length=100,blank=True)#y al departamento que pertenece 
    campus= models.CharField(max_length=100,blank=True)
    foto_Perfil = models.ImageField('Imagen de Perfil', upload_to='dep_mantenimiento/img', blank=True, null= True)
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'trabajador'
        verbose_name = 'Perfil de trabajador'

    
class Solicitud_Mantenimiento(models.Model):
    id = models.AutoField(primary_key=True)
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
        ('En proceso','En proceso'),
        ('En espera','En espera')
        
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
    
    class Meta:
        app_label = 'dep_mantenimiento'
        db_table = 'solicitud mantenimiento'
        verbose_name = 'Solicitud de mantenimiento'


#Asignar permisos a los trabajadores (Docentes, Jefes, Subdirectores) que no pertenece al DEPARTAMENTO DE MANTENIMIENTO DE EQUIPO
#Estos pueden solicitar solicitudes, Editar solicitudes, Eliminar solicitudes, Crear solicitudes     
      
      

# Define una función para crear permisos personalizados
# def create_custom_permissions():
#     # Obtiene el contenido para el modelo de Solicitud_Mantenimiento
#     content_type = ContentType.objects.get_for_model(Solicitud_Mantenimiento)

#     # Verifica si los permisos ya existen
#     existing_permissions = Permission.objects.filter(
#         codename__in=['can_create_solicitud_mantenimiento', 'can_edit_solicitud_mantenimiento', 'can_delete_solicitud_mantenimiento'],
#         content_type=content_type,
#     )

#     if existing_permissions.exists():
#         return existing_permissions

#     # Crea los permisos si no existen
#     permission_create = Permission.objects.create(
#         codename='can_create_solicitud_mantenimiento',
#         name='Can create solicitud mantenimiento',
#         content_type=content_type,
#     )

#     permission_edit = Permission.objects.create(
#         codename='can_edit_solicitud_mantenimiento',
#         name='Can edit solicitud mantenimiento',
#         content_type=content_type,
#     )

#     permission_delete = Permission.objects.create(
#         codename='can_delete_solicitud_mantenimiento',
#         name='Can delete solicitud mantenimiento',
#         content_type=content_type,
#     )

#     return permission_create, permission_edit, permission_delete

# # Define una función para asignar permisos a los usuarios específicos
# def assign_permissions_to_specific_users():
#     # Obtiene o crea el grupo para usuarios con permisos de solicitud
#     group, created = Group.objects.get_or_create(name='Usuarios con permisos de solicitud mantenimiento')

#     # Asigna permisos de solicitud al grupo
#     permission_create, permission_edit, permission_delete = create_custom_permissions()
#     group.permissions.add(permission_create, permission_edit, permission_delete)

#     # Filtra los usuarios que no pertenecen al departamento de Mantenimiento de Equipo
#     specific_users = trabajadores.objects.exclude(departamento='Mantenimiento de Equipo')

#     # Asigna los usuarios al grupo
#     for user in specific_users:
#         user.groups.add(group)

# # Llama a la función para asignar permisos a usuarios específicos
# assign_permissions_to_specific_users()
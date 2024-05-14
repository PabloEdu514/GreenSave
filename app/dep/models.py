from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Dep(models.Model):
    user = models.IntegerField(User)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', blank=True, null= True)
    usuario_activo = models.BooleanField(default=True)
    carrera = models.CharField('Carrera', max_length = 200, blank=True, null= True)
    rol = models.CharField('Rol', max_length=40)
    class Meta:
        app_label = 'dep'
        db_table = u'userDep'

class Bitacora(models.Model):
    usuario = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=250)
    fecha = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'Bitacora'
        app_label = 'dep'      
 

    def __str__(self):
        return f'{self.usuario} - {self.fecha.strftime("%d-%m-%Y %H:%M:%S %Z")}'


BITACORA_ACTIONS={'add':"INSERCIÓN",'update':'MODIFICACIÓN','delete':'ELIMINACIÓN'}    
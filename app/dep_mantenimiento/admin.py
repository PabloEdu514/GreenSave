from django.contrib import admin
from dep_mantenimiento.models import trabajadores,Solicitud_Mantenimiento
# from django.contrib.auth.models import Group
#from .models import Usuario

# Register your models here.




admin.site.register(trabajadores)
admin.site.register(Solicitud_Mantenimiento)
# admin.site.register(empleado)
# admin.site.register(dep_mantenimiento)


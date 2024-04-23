from django.contrib import admin
from dep_mantenimiento.models import trabajadores,Solicitud,empleado
#from .models import Usuario

# Register your models here.




admin.site.register(trabajadores)
admin.site.register(Solicitud)
admin.site.register(empleado)
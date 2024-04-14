from django.contrib import admin
from dep_mantenimiento.models import solicitante,jefMantenimiento,jefDepartamento,subdirectora,trabajadores,Solicitud
#from .models import Usuario

# Register your models here.



admin.site.register(solicitante)
admin.site.register(jefMantenimiento)
admin.site.register(jefDepartamento)
admin.site.register(subdirectora)
admin.site.register(trabajadores)
admin.site.register(Solicitud)
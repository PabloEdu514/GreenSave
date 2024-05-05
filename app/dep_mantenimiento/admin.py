from django.contrib import admin
from dep_mantenimiento.models import trabajadores,Solicitud_Mantenimiento,CustomGroup

#from .models import Usuario

# Register your models here.




class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'puesto', 'departamento', 'get_grupos')

    def get_grupos(self, obj):
        return ", ".join([grupo.name for grupo in obj.grupos.all()])

    get_grupos.short_description = 'Grupos'
class SolicitudMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'folio', 'area_solicitante', 'status', 'id_Trabajador', 'id_Jefe_Departamento', 'id_Jefe_Mantenimiento', 'id_Subdirectora', 'id_Empleado')

admin.site.register(trabajadores, TrabajadoresAdmin)
admin.site.register(Solicitud_Mantenimiento, SolicitudMantenimientoAdmin)
admin.site.register(CustomGroup )
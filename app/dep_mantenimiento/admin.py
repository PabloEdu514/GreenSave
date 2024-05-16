from django.contrib import admin
from dep_mantenimiento.models import trabajadores,Solicitud_Mantenimiento,CustomGroup,HistorialSolicitud,imagenesEvidencias

#from .models import Usuario

# Register your models here.




class TrabajadoresAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'puesto', 'departamento', 'get_grupos')

    def get_grupos(self, obj):
        return ", ".join([grupo.name for grupo in obj.grupos.all()])

    get_grupos.short_description = 'Grupos'
class SolicitudMantenimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'folio', 'area_solicitante', 'status', 'id_Trabajador', 'id_Jefe_Departamento', 'id_Jefe_Mantenimiento', 'id_Subdirectora', 'id_Empleado')

class HistorialSolicitudAdmin(admin.ModelAdmin):
    list_display = ('id','solicitud', 'fecha', 'hora', 'nuevo_status')
    list_filter = ('solicitud__status',)  # Filtro por estado de la solicitud

admin.site.register(HistorialSolicitud, HistorialSolicitudAdmin)
admin.site.register(trabajadores, TrabajadoresAdmin)
admin.site.register(Solicitud_Mantenimiento, SolicitudMantenimientoAdmin)
admin.site.register(CustomGroup )
admin.site.register(imagenesEvidencias )
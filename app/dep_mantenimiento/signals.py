from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import trabajadores, CustomGroup

@receiver(post_save, sender=trabajadores)
def asignar_permisos_trabajador(sender, instance, created, **kwargs):
    if created:
        if instance.puesto == 'Jefe':
            if instance.departamento != 'Mantenimiento de Equipo':
                try:
                    grupo, _ = CustomGroup.objects.get_or_create(name='Jefe Departamento')
                    grupo.permisos = ['view_Solicitud_jefeDep', 'change_Solicitud_jefeDep', 'add_Solicitud_jefeDep', 'delete_Solicitud_jefeDep']
                    instance.grupos.add(grupo)
                except CustomGroup.DoesNotExist:
                    pass
            else:
                try:
                    grupo, _ = CustomGroup.objects.get_or_create(name='Jefe de Mantenimiento de Equipo')
                    grupo.permisos = ['view_Solicitud_jefe_Mantenimiento', 'change_Solicitud_jefe_Mantenimiento']
                    instance.grupos.add(grupo)
                except CustomGroup.DoesNotExist:
                    pass
        elif instance.puesto == 'Empleado' and instance.departamento == 'Mantenimiento de Equipo':
            try:
                grupo, _ = CustomGroup.objects.get_or_create(name='Empleado de Mantenimiento de Equipo')
                grupo.permisos = ['view_Solicitud_empleado_Mantenimiento', 'change_Solicitud_empleado_Mantenimiento']
                instance.grupos.add(grupo)
            except CustomGroup.DoesNotExist:
                pass
        elif instance.puesto == 'Subdirector' and instance.departamento == 'Servicios Administrativos':
            try:
                grupo, _ = CustomGroup.objects.get_or_create(name='Subdirectora de Servicios Administrativos')
                grupo.permisos = ['view_Solicitud_subdirector', 'change_Solicitud_subdirector', 'add_Solicitud_subdirector', 'delete_Solicitud_subdirector']
                instance.grupos.add(grupo)
            except CustomGroup.DoesNotExist:
                pass
        else:
            try:
                grupo, _ = CustomGroup.objects.get_or_create(name='Solicitante')
                grupo.permisos = ['view_Solicitud_Solicitante', 'change_Solicitud_Solicitante', 'add_Solicitud_Solicitante', 'delete_Solicitud_Solicitante']
                instance.grupos.add(grupo)
            except CustomGroup.DoesNotExist:
                pass

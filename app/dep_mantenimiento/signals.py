from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import trabajadores, CustomGroup

@receiver(post_save, sender=trabajadores)
def asignar_permisos_trabajador(sender, instance, created, **kwargs):
    if created:
        grupo_name = None
        if instance.puesto == 'Jefe':
            if instance.departamento != 'Mantenimiento de Equipo':
                grupo_name = 'Jefe Departamento'
            else:
                grupo_name = 'Jefe de Mantenimiento de Equipo'
        elif instance.puesto == 'Empleado' and instance.departamento == 'Mantenimiento de Equipo':
            grupo_name = 'Empleado de Mantenimiento de Equipo'
        elif instance.puesto == 'Subdirector' and instance.departamento == 'Servicios Administrativos':
            grupo_name = 'Subdirectora de Servicios Administrativos'
        else:
            grupo_name = 'Solicitante'
        
        if grupo_name:
            grupo, _ = CustomGroup.objects.get_or_create(name=grupo_name)
            instance.grupos.add(grupo)

@receiver(post_save, sender=trabajadores)
def asignar_grupo(sender, instance, created, **kwargs):
    if created:
        if instance.puesto == 'Jefe':
            if instance.departamento != 'Mantenimiento de Equipo':
                grupo_name = 'Jefe Departamento'
            else:
                grupo_name = 'Jefe de Mantenimiento de Equipo'
        elif instance.puesto == 'Empleado' and instance.departamento == 'Mantenimiento de Equipo':
            grupo_name = 'Empleado de Mantenimiento de Equipo'
        elif instance.puesto == 'Subdirector' and instance.departamento == 'Servicios Administrativos':
            grupo_name = 'Subdirectora de Servicios Administrativos'
        else:
            grupo_name = 'Solicitante'
        
        grupo, _ = CustomGroup.objects.get_or_create(name=grupo_name)
        instance.grupos.add(grupo)
        instance.save()
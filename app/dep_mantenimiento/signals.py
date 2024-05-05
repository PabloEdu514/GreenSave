from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import trabajadores, CustomGroup

@receiver(post_save, sender=trabajadores)
def asignar_permisos_trabajador(sender, instance, created, **kwargs):
    if created:
        # Verificar el puesto y el departamento del trabajador
        if instance.puesto in ['Jefe', 'Empleado'] and instance.departamento == 'Mantenimiento de Equipo':
            try:
                grupo_mantenimiento = CustomGroup.objects.get(name='Trabajadores de Mantenimiento')
                instance.grupos.add(grupo_mantenimiento)
            except CustomGroup.DoesNotExist:
                pass
        else:
            try:
                grupo_solicitantes = CustomGroup.objects.get(name='Usuarios Solicitantes')
                instance.grupos.add(grupo_solicitantes)
            except CustomGroup.DoesNotExist:
                pass

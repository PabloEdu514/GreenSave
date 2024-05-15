from .models import Solicitud_Mantenimiento, CustomGroup

# Obtener los permisos personalizados
permisos_personalizados = Solicitud_Mantenimiento._meta.permissions

# Filtrar permisos para mantenimiento y solicitantes
permisos_mantenimiento = [
    permiso for permiso in permisos_personalizados 
    if "Mantenimiento" in permiso[0]
]

permisos_solicitantes = [
    permiso for permiso in permisos_personalizados 
    if "Solicitantes" in permiso[0]
]


# Crear los grupos
grupo_mantenimiento = CustomGroup.objects.create(name='Trabajadores de Mantenimiento')
grupo_solicitantes = CustomGroup.objects.create(name='Usuarios Solicitantes')

# Asignar los permisos personalizados a los grupos
for permiso in permisos_mantenimiento:
    grupo_mantenimiento.permissions.add(permiso)

for permiso in permisos_solicitantes:
    grupo_solicitantes.permissions.add(permiso)
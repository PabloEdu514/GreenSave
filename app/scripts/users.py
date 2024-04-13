# #Comentar todo esto despues de correr el servidor
from django.contrib.auth.models import User, Group

def run():

 
    #Crea los grupos de la BD
    Group.objects.get_or_create(name='admin_dep')
    Group.objects.get_or_create(name='admin_sarh')
    Group.objects.get_or_create(name='dep')
    Group.objects.get_or_create(name='ca')
    Group.objects.get_or_create(name='se')
    Group.objects.get_or_create(name='fin')
    Group.objects.get_or_create(name='rh')

    User.objects.all().delete()


    # # Create user and save to the database
    try :
        User.objects.get(username='administradorsarh')
    except User.DoesNotExist:
        user = User.objects.create_user('administradorsarh', '', 'holamundo')#crea el usuario 
        grupo = Group.objects.get(name='admin_sarh')#busca el grupo admin
        user.groups.add(grupo.id)#añade el usuario al gurpo admin_sarh
        user.is_superuser = 1#hace que el usuario sea un super usuario
        user.is_staff = 1#hace que el usuario sea staff, esto permite iniciar sesión en el administrador de django
        user.save()#guarda el cambio de la linea anterior


        # # Create user and save to the database
    try :
        User.objects.get(username='administradordep')
    except User.DoesNotExist:
        user = User.objects.create_user('administradordep', '', 'holamundo')#crea el usuario 
        grupo = Group.objects.get(name='admin_dep')#busca el grupo admin
        user.groups.add(grupo.id)#añade el usuario al gurpo admin_sarh
        user.is_superuser = 1#hace que el usuario sea un super usuario
        user.is_staff = 1#hace que el usuario sea staff, esto permite iniciar sesión en el administrador de django
        user.save()#guarda el cambio de la linea anterior

    

    my_function()

def my_function():
  print("Script Completado") 

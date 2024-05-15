from django.db import models
from django.contrib.auth.models import User

class Empleados(models.Model):
    user = models.IntegerField(User)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', blank=True, null= True)
    usuario_activo = models.BooleanField(default=True)
    carrera = models.CharField('Carrera', max_length = 200, blank=True, null= True)
    rol = models.CharField('Rol', max_length=40)
    class Meta:
        app_label = 'Empleados'
        db_table = u'userDep'


#class UsuarioManager(BaseUserManager):
#    class Meta:
#        app_label = 'dep'

#    def create_user(self,email,username,nombres,apellidos,carrera,password = None):
#        if not email:
#            raise ValueError('Favor de ingresar un correo electrónico!')

#        usuario = self.model(
#            username = username, 
#            email = self.normalize_email(email), 
#            nombres = nombres, 
#            apellidos = apellidos,
#            carrera = carrera
#        )

#        usuario.set_password(password)
#        usuario.save()
#        return usuario

#   def create_superuser(self,email,username,nombres,apellidos,password, carrera = None):
#        usuario = self.create_user(
#            email,
#            username=username,
#            nombres=nombres,
#            apellidos=apellidos,
#            carrera=carrera,
#            password=password
#        )
#        usuario.rol = "admin"
#        usuario.save()
#        return usuario
    
#   def create_dep_user(self,email,username,nombres,apellidos,password,carrera):
#        usuario = self.create_user(
#            email=email,
#            username=username,
#            nombres=nombres,
#            apellidos=apellidos,
#            carrera=carrera,
#            password=password
#        )
#        usuario.rol = "dep"
#        usuario.save()
#        return usuario

#    def create_se_user(self,email,username,nombres,apellidos,password,carrera):
#        usuario = self.create_user(
#            email,
#            username=username,
#            nombres=nombres,
#            apellidos=apellidos,
#            carrera=carrera,
#            password=password
#        )
#        usuario.rol = "se"
#        usuario.save()
#        return usuario

#    def create_conta_user(self,email,username,nombres,apellidos,password,carrera):
        # usuario = self.create_user(
        #     email,
        #     username=username,
        #     nombres=nombres,
        #     apellidos=apellidos,
        #     carrera=carrera,
        #     password=password
        # )
        # usuario.rol = "fin"
        # usuario.save()
        # return usuario
    
#    def create_ca_user(self,email,username,nombres,apellidos,password,carrera):
#         usuario = self.create_user(
#             email=email,
#             username=username,
#             nombres=nombres,
#             apellidos=apellidos,
#             carrera=carrera,
#             password=password
#         )
#         usuario.rol = "ca"
#         usuario.save()
#         return usuario

    

# class Usuario(AbstractBaseUser):
#     username = models.CharField('Nombre de Usuario', max_length = 100, unique=True)
#     email = models.EmailField('Correo Electronico', max_length = 254, unique = True)
#     nombres = models.CharField('Nombres', max_length = 200, blank = True, null = True)
#     apellidos = models.CharField('Apellidos', max_length = 200, blank = True, null = True)
#     imagen = models.ImageField('Imagen de Perfil', upload_to='perfil/', blank=True, null= True)
#     usuario_activo = models.BooleanField(default=True)
#     carrera = models.CharField('Carrera', max_length = 200, blank=True, null= True)
#     rol = models.CharField('Rol', max_length=40)
#     objects = UsuarioManager()

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email','nombres','apellidos']

#     def __str__(self):
#         return f'{self.nombres},{self.apellidos}'

#     def has_perm(self, perm, obj = None):
#         return True

#     def has_module_perms(self, app_label):
#         return True
    

#     @property
#     def is_staff(self):
#         return self.rol

#     class Meta:
#         app_label = 'dep'
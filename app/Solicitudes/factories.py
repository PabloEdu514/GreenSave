import factory
from faker import Faker

from .models import Usuario

fake = Faker()

class UsuarioDEPFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
    
    email = f'{fake.first_name().lower()}-{fake.last_name().lower()}_DEP@morelia.tecnm.mx'
    username =fake.first_name()
    nombres = fake.name()
    apellidos =fake.last_name()
    password = fake.msisdn()
    rol = "dep"

class UsuarioSEFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
    
    email = f'{fake.first_name().lower()}-{fake.last_name().lower()}_SE@morelia.tecnm.mx'
    username =fake.first_name()
    nombres = fake.name()
    apellidos =fake.last_name()
    password = fake.msisdn()
    rol = "se"

class UsuarioFinancieroFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
    
    email = f'{fake.first_name().lower()}-{fake.last_name().lower()}_FINANCIERO@morelia.tecnm.mx'
    username =fake.first_name()
    nombres = fake.name()
    apellidos =fake.last_name()
    password = fake.msisdn()
    rol = "financiero"
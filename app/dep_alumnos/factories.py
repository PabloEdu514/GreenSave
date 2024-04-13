import factory
from faker import Faker
import random
from datetime import datetime

from .models import Solicitud, Status, Tipo

fake = Faker()
carreras = ["CONTADOR PÚBLICO",
            "LIC. EN ADMINISTRACIÓN",
            "LIC. EN ADMINISTRACIÓN (EDUCACIÓN A DISTANCIA)",
            "ING. EN GESTIÓN EMPRESARIAL",
            "ING. INDUSTRIAL",
            "ING. INDUSTRIAL (EDUCACIÓN A DISTANCIA)",
            "ING. BIOQUÍMICA",
            "ING. ELÉCTRICA",
            "ING. ELECTRÓNICA",
            "ING. MECÁNICA",
            "ING. MECATRÓNICA",
            "ING. EN MATERIALES",
            "ING. EN SISTEMAS COMPUTACIONALES",
            "ING. EN TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN"]
now = datetime.now()

#-------- Subfactories de Status --------

class Status3SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 3
    descripcion = "Documentos pendientes"

class Status4SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 4
    descripcion = "Recibida por DEP"

class Status5SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 5
    descripcion = "Validada"

class Status7SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 7
    descripcion = "Finalizada"

class Status8SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 8
    descripcion = "Cancelada"

class Status10SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Status
    idstatus = 10
    descripcion = "Rechazada"

#-------- Subfactories de Tipo --------

class Tipo1SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tipo
    idtipo = 1
    descripcion = "Prorroga"

class Tipo2SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tipo
    idtipo = 2
    descripcion = "Comite"

class Tipo3SubFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tipo
    idtipo = 3
    descripcion = "Cambio de carrera"

#-------- Factory para Comite --------

class SolicitudComiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.M.001-{now.year}'
    idtipo = factory.SubFactory(Tipo2SubFactory)
    idstatus = factory.SubFactory(Status3SubFactory)
    fechainicio = fake.date()
    asunto = "Baja de materias"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)

#-------- Factory para Prorroga de Comite --------

class SolicitudProrrogaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.M.002-{now.year}'
    idtipo = factory.SubFactory(Tipo1SubFactory)
    idstatus = factory.SubFactory(Status4SubFactory)
    fechainicio = fake.date()
    asunto = "Prorroga a semestre 13"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)
    referencia_pago_referencia = fake.iban()

#-------- Factory para Cambio de carrera --------

class SolicitudCambioCarreraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.A.001-{now.year}'
    idtipo = factory.SubFactory(Tipo3SubFactory)
    idstatus = factory.SubFactory(Status5SubFactory)
    fechainicio = fake.date()
    asunto = "Cambio de Mecanica a ISC"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)
    referencia_pago_referencia = fake.iban()

#-------- Factory para solicitud finalizada --------

class SolicitudFinalizadaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.M.003-{now.year}'
    idtipo = factory.SubFactory(Tipo2SubFactory)
    idstatus = factory.SubFactory(Status7SubFactory)
    fechainicio = fake.date()
    fechafinal = fake.date()
    asunto = "Renuncia de creditos"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)
    respuesta = "Aprobada"

#-------- Factory para solicitud cancelada --------

class SolicitudCanceladaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.M.004-{now.year}'
    idtipo = factory.SubFactory(Tipo1SubFactory)
    idstatus = factory.SubFactory(Status8SubFactory)
    fechainicio = datetime.now()
    fechafinal = datetime.now()
    asunto = "Prorroga semestre 14"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)
    referencia_pago_referencia = fake.iban()
    cancelacion = "No lo ocupe"
    respuesta = "Cancelada"

#-------- Factory para solicitud rechazada --------

class SolicitudRechazadaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Solicitud
    
    idfolio = f'C.A.002-{now.year}'
    idtipo = factory.SubFactory(Tipo3SubFactory)
    idstatus = factory.SubFactory(Status10SubFactory)
    fechainicio = datetime.now()
    fechafinal = datetime.now()
    asunto = "Cambio de Materiales a ISC"
    nombre = fake.name()
    carrera = random.choice(carreras)
    primer_apellido = fake.last_name()
    semestre = fake.pyint(1,12)
    referencia_pago_referencia = fake.iban()
    respuesta = "Rechazada"
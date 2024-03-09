from django.db import models
from .validators import validate_file_extension

class Solicitud(models.Model):
    idfolio = models.CharField(max_length=45, primary_key=True)
    idtipo = models.ForeignKey('Tipo', models.DO_NOTHING, db_column='idtipo')
    idstatus = models.ForeignKey('Status', models.DO_NOTHING, db_column='idstatus')
    fechainicio = models.CharField(max_length=100, blank=True, null=True)
    fechafinal = models.CharField(max_length=100, blank=True, null=True)
    asunto = models.TextField(blank=True, null=True)
    nocontrol = models.CharField(max_length=9, blank=True, null=True)
    nombre = models.CharField(max_length=45)
    carrera = models.CharField(max_length=60, blank=True, null=True)
    especialidad = models.CharField(max_length=45, blank=True, null=True)
    telefono = models.CharField(max_length=45, blank=True, null=True)
    correo = models.CharField(max_length=45, blank=True, null=True)
    sexo = models.CharField(max_length=45, blank=True, null=True)
    primer_apellido = models.CharField(max_length=45)
    segundo_apellido = models.CharField(max_length=45, blank=True, null=True)
    semestre = models.IntegerField(blank=True, null=True)
    referencia_pago_referencia = models.CharField(max_length=45, blank=True, null=True)
    motivo = models.TextField(blank=True, null=True)
    cancelacion = models.TextField(blank=True, null=True)
    doc_solicitud = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    doc_kardex = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    doc_comprobante = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    doc_otro = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    doc_examen = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    doc_comba = models.FileField(max_length=150,blank=True, null=True, validators=[validate_file_extension])
    responsable = models.CharField(max_length=45, blank=True, null=True)
    respuesta = models.CharField(max_length=250, blank=True, null=True)
    fechalimite = models.DateField(blank=True, null=True)
    status_referencia = models.CharField(max_length=45, blank=True, null=True)
    carrera_destino= models.CharField(max_length=60, blank=True, null=True)
        #Aqui empece mis cosas
    status_dictamen = models.CharField(max_length=45, blank=True, null=True)
        #Aqui acabe mis cosas
    folio_final = models.CharField(max_length=45, blank=True, null=True)     


    def __str__(self):
        return self.folio

    
    class Meta:
        managed = True
        db_table = 'solicitud'
        app_label = 'dep'


class Status(models.Model):
    idstatus = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return self.descripcion

    class Meta:
        managed = True
        db_table = 'status'
        app_label = 'dep'


class Tipo(models.Model):
    idtipo = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    proceso_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


    class Meta:
        managed = True
        db_table = 'tipo'
        app_label = 'dep'

class Precios(models.Model):
    idprecio = models.TextField(primary_key=True, max_length=45, blank=True, null=False)
    precio = models.FloatField(blank=True, null=True)    

    def __str__(self):
        return self.precio

    class Meta:
        managed = True
        db_table = 'precios'
        app_label = 'dep'

class Counters(models.Model):
    idcounter = models.TextField(primary_key=True, max_length=45, blank=True, null=False)
    counter = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.counter

    class Meta:
        managed = True
        db_table = 'counters'
        app_label = 'dep'

class tokens(models.Model):
    idtoken = models.AutoField(primary_key=True)
    token = models.CharField(max_length=45, blank=True)
    token_activo = models.BooleanField(default=True)

    def __str__(self):
        return self.token

    class Meta:
        managed = True
        db_table = 'tokens'
        app_label = 'dep'

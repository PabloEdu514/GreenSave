from django import forms
from dep_alumnos.models import tokens
from .models import Solicitud_Mantenimiento, imagenesEvidencias, trabajadores
from django.forms.widgets import TextInput, FileInput, ClearableFileInput, DateInput, SelectMultiple



class SolicitudMantenimientoForm(forms.Form):
   
    folio = forms.CharField(label='Folio', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el folio'}))
    tipos_servicio = forms.ChoiceField(label='Tipo de Servicio', choices=[
        ('', 'Seleccionar'),
        ('Electrica', 'Electrica'),
        ('Herrería', 'Herrería'),
        ('Plomería', 'Plomería'),
        ('Pintura', 'Pintura'),
        ('Cañones', 'Cañones'),
        ('Pintarrón', 'Pintarrón'),
        ('Cerrajería', 'Cerrajería'),
        ('Otro', 'Otro'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    descripcion = forms.CharField(label='Descripción del Servicio o Falla a Reparar', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}))
    des_Serv_no_Realizado = forms.CharField(label='Descripción del por qué no se puede realizar', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}), required=False)
    motv_rechazo = forms.CharField(label='Descripción del por qué no se puede realizar', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}), required=False)
    des_Serv_Realizado = forms.CharField(label='Descripción del trabajo o servicio realizado', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}), required=False)
    material_utilizado = forms.CharField(label='Material utilizado', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}), required=False)
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'class': 'form-control', 'readonly': True}))  # Campo de solo lectura para la fecha
    area_solicitante = forms.CharField(label='Área Solicitante', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))  # Campo de solo lectura para el área solicitante
    responsable_Area = forms.CharField(label='Responsable del Área', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))  # Campo de solo lectura para el responsable del área

class JefeForm(forms.Form):
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    folio = forms.CharField(label='Folio', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el folio'}))
    area_solicitante = forms.CharField(label='Área Solicitante', widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    responsable_Area = forms.CharField(label='Responsable del Área', widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    tipo_servicio = forms.ChoiceField(label='Tipo de Servicio', choices=[
        ('', 'Seleccionar'),
        ('Electrica', 'Electrica'),
        ('Herrería', 'Herrería'),
        ('Plomería', 'Plomería'),
        ('Pintura', 'Pintura'),
        ('Cañones', 'Cañones'),
        ('Pintarrón', 'Pintarrón'),
        ('Cerrajería', 'Cerrajería'),
        ('Otro', 'Otro'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    descripcion = forms.CharField(label='Descripción del Servicio o Falla a Reparar', widget=forms.Textarea(attrs={'class': 'form-control'}))
    firma_Jefe_Departamento_img = forms.FileField(label='Firma del Jefe de Departamento', widget=forms.FileInput(attrs={'class': 'form-control'}))

class firmar_Formulario(forms.Form):
    firma_Jefe_Departamento_img = forms.FileField(label='Firma del Jefe de Departamento', widget=forms.FileInput(attrs={'class': 'form-control'}))     # Campo para cargar la firma para el responsable del área     
    #Estos campos son para mostrar la información de la BD
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    folio = forms.CharField(label='Folio', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    area_solicitante = forms.CharField(label='Área Solicitante', widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    responsable_Area = forms.CharField(label='Responsable del Área', widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    tipo_servicio = forms.ChoiceField(label='Tipo de Servicio',widget=forms.TextInput(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    descripcion = forms.CharField(label='Descripción del Servicio o Falla a Reparar', widget=forms.Textarea(attrs={'class': 'form-control-plaintext', ' readonly': True}))
    
    
class firma_Formulario_Empleado(forms.Form):
    material_utilizado= forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el material que utilizo', 'rows': 2}))
    des_Serv_Realizado=forms.CharField( widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción de como realizo el trabajo', 'rows': 2}))
    firma_Empleado_img= forms.FileField( widget=forms.FileInput(attrs={'class': 'form-control'}))
    
        
class Evidencias(forms.ModelForm):            
        class Meta:
            model = imagenesEvidencias
            fields = ['evidenciasIMG']
            labels={
             
                'evidenciasIMG': '',
            }
            widgets = {
               
                'evidenciasIMG': ClearableFileInput(attrs={
                    "name": "images",
                    "class": "form-control",
                }),
               
            } 
            
            
            

class SolicitudAsignar(forms.Form):
    material_Asignado = forms.CharField(label='Material utilizado', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 2}))
    empleado = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener todos los empleados que cumplen con los criterios especificados
        empleados = trabajadores.objects.filter(puesto='Empleado', departamento='Mantenimiento de Equipo').order_by('nombres', 'appaterno', 'apmaterno')
        # Cargar las opciones de empleados en el ChoiceField del formulario
        self.fields['empleado'].choices = [(empleado.id, empleado.nombre_completo()) for empleado in empleados]
        
        # Si el campo empleado ya tiene un valor, hacerlo de solo lectura
        if 'initial' in kwargs and kwargs['initial'].get('empleado'):
            self.fields['empleado'].widget.attrs['readonly'] = True   
            
            
class firmaVoBoForm(forms.Form):
    firma_Jefe_VoBo_img = forms.FileField( widget=forms.FileInput(attrs={'class': 'form-control'}))     # Campo para cargar la firma para el firma_Jefe_VoBo_img         
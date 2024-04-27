from django import forms
from dep_alumnos.models import tokens
from .models import Solicitud_Mantenimiento

class tokensForm(forms.ModelForm):
    class Meta:
        model = tokens
        exclude = ('idtoken','token_activo')
        

class SolicitudMantenimientoForm(forms.Form):
    fecha = forms.DateField(label='Fecha', widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Seleccione la fecha'}))
    folio = forms.CharField(label='Folio', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el folio'}))
    area_solicitante = forms.CharField(label='Área Solicitante', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el área solicitante'}))
    responsable_area = forms.CharField(label='Responsable del Área', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el responsable del área'}))
    tipos_servicio = forms.ChoiceField(label='Tipo de Servicio', choices=[
        ('', 'Seleccionar'),
        ('Electrica','Electrica'),
        ('Herrería','Herrería'),
        ('Plomería','Plomería'),
        ('Pintura','Pintura'),
        ('Cañones','Cañones'),
        ('Pintarrón','Pintarrón'),
        ('Cerrajería','Cerrajería'),
        ('Otro','Otro')
    ], widget=forms.Select(attrs={'class': 'form-select'}))
    descripcion = forms.CharField(label='Descripción del Servicio o Falla a Reparar', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción', 'rows': 5}))
    id_Trabajador=forms.IntegerField()
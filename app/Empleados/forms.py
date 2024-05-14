from django import forms
from dep_alumnos.models import tokens

class tokensForm(forms.ModelForm):
    class Meta:
        model = tokens
        exclude = ('idtoken','token_activo')
        
class SolicitudForm(forms.Form):
    fecha = forms.DateField(label="Fecha")
    folio = forms.CharField(label="Folio")
    area_solicitante = forms.CharField(label="Área Solicitante")
    responsable_area = forms.CharField(label="Responsable del Área")
    tipos_servicio = forms.ChoiceField(label="Tipo de Servicio", choices=[("tipo1", "Tipo 1"), ("tipo2", "Tipo 2"), ("tipo3", "Tipo 3")])
    descripcion = forms.CharField(label="Descripción del Servicio o Falla a Reparar", widget=forms.Textarea)

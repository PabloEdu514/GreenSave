from django import forms
from dep_alumnos.models import tokens

class tokensForm(forms.ModelForm):
    class Meta:
        model = tokens
        exclude = ('idtoken','token_activo')
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Dep
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from .models import Bitacora,BITACORA_ACTIONS
class Error404Views(TemplateView):
    template_name="404.html"

# Create your views here.

def dashboard(request):
    
    context = {}
    Bitacora.objects.create(usuario=1,descripcion='Prueba de bitacora')
    return render(request, 'dep/layout/home.html', context)

def bitacora(usuario,modelo='',accion='',detalles='',token='',**kwargs):
    dif=kwargs.get('Departamento')
    descripcion = f'{dif}/{modelo.upper()}/{BITACORA_ACTIONS.get(accion)}'
   
    if detalles:
        descripcion+=f'/{detalles}'
    if token:
        descripcion+=f'/{token}'
    Bitacora.objects.create(usuario=usuario,descripcion=descripcion)


@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

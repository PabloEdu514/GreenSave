from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import dep_mantenimiento
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse

class Error404Views(TemplateView):
    template_name="404.html"

# Create your views here.

def dashboard_solicitante(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/solicitante/home.html', context)
def dashboard_solformulario(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/solicitante/formulario.html', context)

def dashboard_empleado(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/empleado/home.html', context)

def dashboard_empleado_firma_form(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/empleado/firma_form.html', context)


def dashboard_subdirectora(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/subdirectora/home.html', context)
def dashboard_subd_formulario(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/subdirectora/formulario.html', context)

def dashboard_subdpeticion_form(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/subdirectora/peticion_form.html', context)
def dashboard_subrechazar_form(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/subdirectora/rechazar_form.html', context)

def dashboard_jDep(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jDep/home.html', context)

def dashboard_jDepformulario(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jDep/formulario.html', context)
def dashboard_jDepfirmar_form(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jDep/firma_form.html', context)


def dashboard_jMantenimeinto(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jMantenimiento/home.html', context)
def dashboard_jMantenimeinto_firmar(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jMantenimiento/firma_form_VoBo.html', context)
def dashboard_jMantenimeinto_rechazar(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jMantenimiento/rechazar_form.html', context)
def dashboard_jMantenimeinto_estatus(request):
    context = {}
    return render(request, 'dep_mantenimiento/layout/jMantenimiento/estatus.html', context)

@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

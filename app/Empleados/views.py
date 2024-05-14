from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Empleados
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from .forms import SolicitudForm

class Error404Views(TemplateView):
    template_name="404.html"

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, 'Empleados/layout/home.html', context)



@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def solicitud_view(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            # Procesar el formulario si es válido
            # Aquí puedes guardar la información en la base de datos, enviar correos, etc.
            pass
    else:
        form = SolicitudForm()
    return render(request, 'solicitud_template.html', {'form': form})

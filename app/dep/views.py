from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Dep
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse

class Error404Views(TemplateView):
    template_name="404.html"

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, 'dep/layout/home.html', context)


@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

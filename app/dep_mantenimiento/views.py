from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import View
from .models import Solicitud,solicitante
from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.db import transaction

class Views_Solicitantes(View):
    
    @staticmethod
    def get(request, id_solicitante=1):
        try:
            # Obtenemos el solicitante
            id_sol = solicitante.objects.get(id=id_solicitante)
            # Filtramos las solicitudes asociadas al solicitante y las ordenamos por fecha de manera descendente
            solicitudes = Solicitud.objects.filter(solicitante=id_sol).order_by('-fecha','-hora')
            # Verificamos si se encontraron solicitudes
            if solicitudes.exists():
                # Creamos una lista para almacenar las solicitudes con el tiempo transcurrido
                solicitudes_con_tiempo = []
                # Obtenemos la fecha y hora actual
                now = datetime.now()
                # Recorremos las solicitudes
                for solicitud in solicitudes:
                    # Calculamos el tiempo transcurrido
                    tiempo_transcurrido = now - datetime.combine(solicitud.fecha, solicitud.hora)
                    # Convertimos el tiempo transcurrido a segundos
                    tiempo_transcurrido_segundos = tiempo_transcurrido.total_seconds()
                    # Añadimos el tiempo transcurrido como un nuevo campo al diccionario de la solicitud
                    solicitud_dict = {
                        'tipo_servicio': solicitud.tipo_servicio,
                        'descripcion': solicitud.descripcion,
                        'status': solicitud.status,
                        'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formateamos la fecha como dd/mm/aaaa
                        'hora': solicitud.hora.strftime("%H:%M"),  # Formateamos la hora como hh:mm
                        'tiempo_transcurrido': tiempo_transcurrido_segundos  # Añadimos el tiempo transcurrido en segundos
                    }
                    # Agregamos la solicitud con el tiempo transcurrido a la lista
                    solicitudes_con_tiempo.append(solicitud_dict)
                
                # Creamos el contexto con las solicitudes y su tiempo transcurrido
                contexto = {'Solicitudes': solicitudes_con_tiempo}
                # Renderizamos la plantilla y pasamos el contexto como datos
                return render(request, 'dep_mantenimiento/layout/solicitante/home.html', contexto)
            else:
                # Si no se encontraron solicitudes, retornamos un mensaje de error
                return JsonResponse({'message': "Solicitudes no encontradas"})
        except solicitante.DoesNotExist:
            # Si el solicitante no existe, lanzamos una excepción Http404
            raise Http404("El solicitante no existe")
@staticmethod 
def delete(request, id_solicitud):
    try:
        with transaction.atomic():
            # Eliminar la solicitud
            solicitud = Solicitud.objects.get(id=id_solicitud)
            solicitud.delete()
            
            # Redirigir a la página principal o actualizar la tabla de solicitudes
            return HttpResponseRedirect('/dep_mantenimiento/solicitante/inicio/')
    except Solicitud.DoesNotExist:
        # Si la solicitud no existe, lanzar una excepción Http404
        raise Http404("La solicitud no existe")


class Error404Views(TemplateView):
    template_name="404.html"
Solicitante = None
def guardar_datos(request):
    if request.method == 'POST':
        Solicitante = solicitante.objects.get(id=1)
        id_fecha = request.POST.get('fecha')
        id_folio = request.POST.get('folio')
        id_area_solicitante = request.POST.get('area_solicitante')
        id_responsable_area = request.POST.get('responsable_Area')  
        id_tipos_servicio = request.POST.get('tipos_servicio')
        id_descripcion = request.POST.get('descripcion')
        hora_actual = datetime.now().time()
        # Crea una instancia de tu modelo Solicitud y asigna los valores
        datos_nuevos = Solicitud(
            solicitante=Solicitante,
            fecha=id_fecha,
            folio=id_folio,
            area_solicitante=id_area_solicitante,
            responsable_Area=id_responsable_area,  # Utiliza el mismo nombre que en el modelo
            tipo_servicio=id_tipos_servicio,
            descripcion=id_descripcion,
            hora=hora_actual
        )
        
        # Guarda los datos en la base de datos
        datos_nuevos.save()

        # Redirige a alguna página de éxito o renderiza una plantilla
        #return redirect('pagina_exito')

    return render(request, 'dep_mantenimiento/layout/solicitante/formulario.html')

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




#@perssion  
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

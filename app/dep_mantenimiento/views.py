from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import logout
from django.views import View

from django.http import Http404
from django.views.generic import TemplateView
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
from django.utils import timezone
from django.db import transaction
from .models import Solicitud_Mantenimiento,trabajadores
from django.shortcuts import redirect
from datetime import datetime

@login_required

def inicio(request):
    user = request.user
    if user.is_authenticated:
        try:
            id_trabajador = trabajadores.objects.get(user=user.id)
            
            if id_trabajador.puesto == 'Jefe' and id_trabajador.departamento != 'Mantenimiento de Equipo':
                            return redirect('inicio_jefe_departamento')  # Redireccionar al inicio del jefe de otro departamento
            elif id_trabajador.puesto == 'Docente':
                        # Redirigir a la página de inicio del docente
                        return redirect('inicio_docente', id=id_trabajador.id) 
            elif id_trabajador.puesto == 'Subdirector':
                            if  id_trabajador.departamento == 'Servicios Administrativos':
                                return redirect('inicio_subdirector_servicios')  # redireccionar al inicio subdirectora de servicios
                            else:
                                return redirect('inicio_subdirector')  # redireccionar al inicio subdirectorato
                        
                  
          
            elif id_trabajador.puesto == 'Jefe' and id_trabajador.departamento == 'Mantenimiento de Equipo':
                        return redirect('inicio_jefe_mantenimiento')  # Redireccionar al inicio de jefe de mantenimiento del departamento de Mantenimiento de Equipo
            elif id_trabajador.puesto == 'Empleado'and id_trabajador.departamento == 'Mantenimiento de Equipo':
                        return redirect('inicio_empleado')  # Redireccionar al inicio de un empleado del departamento de Mantenimiento de Equipo
            else:
                    # Mostrar un mensaje de alerta para otros usuarios con permisos de solicitud
                    messages.warning(request, 'Tu perfil no tiene una página de inicio asignada. Contacta al administrador.')
                    return redirect('inicio_usuario')  # Redireccionar al inicio de otros usuarios con permisos de solicitud
        except trabajadores.DoesNotExist:
            return redirect('login')  # Redireccionar al inicio de sesión si el usuario no está autenticado
    return redirect('login')  # Redireccionar al inicio de sesión si el usuario no está autenticado



#Vistas para el Docente
class vistas_solicitantes_cargar_inicio(View):
    @staticmethod
    def cargar_Inicio(request, id):
        # Lógica para determinar el tipo de usuario
        es_docente = True  # Por ejemplo, asumamos que el usuario es un docente

        if es_docente:
            
            url_inicio = reverse('inicio_docente', args=[id])  # Asegúrate de pasar el id adecuado aquí
        else:
            url_inicio = reverse('inicio')

        contexto = {
            'id': id,
            'url_inicio': url_inicio
        }

        return render(request, 'dep_mantenimiento/layout/solicitante/home.html', contexto)
   
    @staticmethod
    def obtener_solicitudes(request, id_Docente):
        try:
            # Filtrar las solicitudes asociadas al docente
            solicitudes = Solicitud_Mantenimiento.objects.filter(id_Trabajador=id_Docente).order_by('-fecha', '-hora')
            
            # Verificar si se encontraron solicitudes
            if solicitudes.exists():
                # Crear una lista para almacenar las solicitudes con el tiempo transcurrido
                solicitudes_con_tiempo = []
                # Obtener la fecha y hora actual
                now = datetime.now()
                # Recorrer las solicitudes
                for solicitud in solicitudes:
                    # Calcular el tiempo transcurrido
                    tiempo_transcurrido = now - datetime.combine(solicitud.fecha, solicitud.hora)
                    # Convertir el tiempo transcurrido a segundos
                    tiempo_transcurrido_segundos = tiempo_transcurrido.total_seconds()
                    # Añadir el tiempo transcurrido como un nuevo campo al diccionario de la solicitud
                    solicitud_dict = {
                        'id': solicitud.id,
                        'tipo_servicio': solicitud.tipo_servicio,
                        'descripcion': solicitud.descripcion,
                        'status': solicitud.status,
                        'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                        'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                        'tiempo_transcurrido': tiempo_transcurrido_segundos  # Añadir el tiempo transcurrido en segundos
                    }
                    # Agregar la solicitud con el tiempo transcurrido a la lista
                    solicitudes_con_tiempo.append(solicitud_dict)

                # Retornar los datos en formato JSON
                return JsonResponse({'solicitudes': solicitudes_con_tiempo})
            else:
                # Si no se encontraron solicitudes, retornar un mensaje de error
                return JsonResponse({'message': "Solicitudes no encontradas"})
        except Solicitud_Mantenimiento.DoesNotExist:
            # Si la solicitud no existe, lanzar una excepción Http404
             raise Http404("Las solicitudes del docente no existen")
        
        

    
    
    
    

class Error404Views(TemplateView):
    template_name="404.html"




#@perssion  
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



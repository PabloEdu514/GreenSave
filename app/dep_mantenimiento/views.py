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
from .forms import SolicitudMantenimientoForm
from django.db import transaction,connection

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
    def cargar_Formulario(request,id_Docente):
        # Lógica para determinar el tipo de usuario
        es_docente = True  # Por ejemplo, asumamos que el usuario es un docente
        form = SolicitudMantenimientoForm()
        if es_docente:
            
            url_formulario = reverse('formulario_docente', args=[id_Docente])  # Asegúrate de pasar el id adecuado aquí
        else:
            url_formulario = reverse('inicio')

        contexto = {
            'id': id_Docente,
            'url_formulario': url_formulario,
            'form': form,  # Pasar el formulario al contexto
        }
        return render(request, 'dep_mantenimiento/layout/solicitante/formulario.html', contexto)

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
        

def eliminar_solicitud(request, solicitud_id):
    try:
        # Eliminar la solicitud
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        solicitud.delete()

         # Reiniciar la secuencia de IDs de la tabla de la base de datos
         ###
#         with connection.cursor() as cursor:s
#             cursor.execute('ALTER SEQUENCE public.solicitud_mantenimiento_id_seq RESTART WITH 1;')

#             cursor.execute('UPDATE "solicitud_mantenimiento" SET id = id - 1 WHERE id > 1;')    
# ###
        return redirect ('inicio')
    except Solicitud_Mantenimiento.DoesNotExist:
        return JsonResponse({'error': 'La solicitud no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
class rellenar_formulario(View):
    @staticmethod   
     
    def guardar_datos_Docente(request, id_Docente):
        if request.method == 'POST':
            form = SolicitudMantenimientoForm(request.POST)
            if form.is_valid():
                id_fecha = form.cleaned_data['fecha']
                id_folio = form.cleaned_data['folio']
                id_area_solicitante = form.cleaned_data['area_solicitante']
                id_responsable_area = form.cleaned_data['responsable_Area']
                id_tipos_servicio = form.cleaned_data['tipos_servicio']
                id_descripcion = form.cleaned_data['descripcion']
                hora_actual = datetime.now().time()
                # Obtener la instancia del trabajador correspondiente al ID
                trabajador = trabajadores.objects.get(id=id_Docente)
                
                # Crea una instancia del modelo Solicitud y asigna los valores
                datos_nuevos = Solicitud_Mantenimiento(
                    fecha=id_fecha,
                    folio=id_folio,
                    area_solicitante=id_area_solicitante,
                    responsable_Area=id_responsable_area,
                    tipo_servicio=id_tipos_servicio,
                    descripcion=id_descripcion,
                    hora=hora_actual,
                    id_Trabajador=trabajador, # Asignar la instancia del trabajador, no solo el ID
                    status='Enviado',
                )
                
                # Guarda los datos en la base de datos
                datos_nuevos.save()

                # Redirige a la URL de la vista de inicio del docente
                return redirect('inicio_docente', id=id_Docente)
                
        else:
            form = SolicitudMantenimientoForm()
            
        # Renderiza el formulario
        return render(request, 'dep_mantenimiento/layout/solicitante/formulario.html', {'form': form})
    

class Error404Views(TemplateView):
    template_name="404.html"




#@perssion  
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



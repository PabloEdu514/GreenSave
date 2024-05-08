from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404,HttpResponseForbidden
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.models import User, AbstractUser
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
from dep.views import bitacora
from django.core.exceptions import PermissionDenied


def grupo_trabajador_requerido(user):
    if user.is_authenticated:
        try:
            trabajador = trabajadores.objects.get(user_id=user.id)
            # Verificar si el trabajador pertenece al grupo "Jefe Departamento"
            if trabajador.grupos.filter(name='Jefe Departamento').exists():
                return True
            # Verificar si el trabajador pertenece al grupo "Jefe de Mantenimiento de Equipo"
            elif trabajador.grupos.filter(name='Jefe de Mantenimiento de Equipo').exists():
                return True
             # Verificar si el trabajador pertenece al grupo "Empleado de Mantenimiento de Equipo"
            elif trabajador.grupos.filter(name='Empleado de Mantenimiento de Equipo').exists():
                return True
            # Verificar si el trabajador pertenece al grupo "Servicios Administrativos"
            elif trabajador.grupos.filter(name='Servicios Administrativos').exists():
                return True
            # Verificar si el trabajador pertenece al grupo "Solicitante"
            elif trabajador.grupos.filter(name='Solicitante').exists():
                return True            
            else:
                # Si el usuario no pertenece a ninguno de los grupos requeridos, mostrar la página de error 403
                raise PermissionDenied
        except trabajadores.DoesNotExist:
            pass
    # Si el usuario no está autenticado, mostrar la página de error 403
    raise PermissionDenied



@user_passes_test(grupo_trabajador_requerido)
@login_required

def inicio(request):
    user = request.user
    if user.is_authenticated:
        try:
            id_trabajador = trabajadores.objects.get(user_id=user.id)
            
            if id_trabajador.puesto == 'Jefe' and id_trabajador.departamento != 'Mantenimiento de Equipo':
                            return redirect('inicio_jefe_departamento',id=id_trabajador.id)  # Redireccionar al inicio del jefe de otro departamento
            elif id_trabajador.puesto == 'Docente':
                        # Redirigir a la página de inicio del docente
                        return redirect('inicio_docente', id=id_trabajador.id) 
            elif id_trabajador.puesto == 'Subdirector':
                            if  id_trabajador.departamento == 'Servicios Administrativos':
                                return redirect('inicio_subdirector_servicios', id=id_trabajador.id)  # redireccionar al inicio subdirectora de servicios
                            else:
                                return redirect('inicio_docente', id=id_trabajador.id)  # redireccionar al inicio subdirectorato             
          
            elif id_trabajador.puesto == 'Jefe' and id_trabajador.departamento == 'Mantenimiento de Equipo':
                        return redirect('inicio_jefe_mantenimiento', id=id_trabajador.id)  # Redireccionar al inicio de jefe de mantenimiento del departamento de Mantenimiento de Equipo
            elif id_trabajador.puesto == 'Empleado'and id_trabajador.departamento == 'Mantenimiento de Equipo':
                        return redirect('inicio_empleado', id=id_trabajador.id)  # Redireccionar al inicio de un empleado del departamento de Mantenimiento de Equipo
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
    #Jalar datos de la BD
    def cargar_Formulario(request, id_Docente):
        # Lógica para determinar el tipo de usuario
        es_docente = True  # Por ejemplo, asumamos que el usuario es un docente

        # Obtener la fecha actual
        fecha_actual = datetime.now().date()
        trabajador = trabajadores.objects.get(id=id_Docente)
        # Obtener el área solicitante y el responsable del área
        departamento = trabajador.departamento
                
                # Obtener el jefe del departamento
        jefe_departamento = trabajadores.objects.filter(departamento=departamento, puesto='Jefe').first()
                # Verificar si se encontró un jefe para el departamento
        if jefe_departamento:
                    # Obtener el nombre completo del jefe del departamento
                nombre_jefe_departamento = jefe_departamento.nombre_completo()
        else:
                    # Manejar el caso en el que no se encuentre ningún jefe para el departamento
            nombre_jefe_departamento = "No asignado"

        # Crear una instancia del formulario con los valores iniciales
        form = SolicitudMantenimientoForm(initial={
            'fecha': fecha_actual,
            'area_solicitante': departamento,
            'responsable_Area': nombre_jefe_departamento,
        })

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
    @staticmethod   
    def guardar_datos_Docente(request, id_Docente):
        if request.method == 'POST':
            form = SolicitudMantenimientoForm(request.POST)
            if form.is_valid():
                id_fecha = datetime.now().date()
                id_folio = form.cleaned_data['folio']
                id_tipos_servicio = form.cleaned_data['tipos_servicio']
                id_descripcion = form.cleaned_data['descripcion']
                hora_actual = datetime.now().time()
                # Obtener la instancia del trabajador correspondiente al ID
                trabajador = trabajadores.objects.get(id=id_Docente)
                departamento = trabajador.departamento
                
                # Obtener el jefe del departamento
                jefe_departamento = trabajadores.objects.filter(departamento=departamento, puesto='Jefe').first()
                # Verificar si se encontró un jefe para el departamento
                if jefe_departamento:
                    # Obtener el nombre completo del jefe del departamento
                    nombre_jefe_departamento = jefe_departamento.nombre_completo()
               
                else:
                    # Manejar el caso en el que no se encuentre ningún jefe para el departamento
                    nombre_jefe_departamento = "No asignado"  # O puedes manejarlo de otra manera según tu lógica de negocio
                # Crea una instancia del modelo Solicitud y asigna los valores
                datos_nuevos = Solicitud_Mantenimiento(
                    fecha=id_fecha,
                    folio=id_folio,
                    area_solicitante=departamento,
                    responsable_Area=nombre_jefe_departamento,  # Aquí asignamos el jefe del departamento como responsable del área
                    tipo_servicio=id_tipos_servicio,
                    descripcion=id_descripcion,
                    hora=hora_actual,
                    id_Trabajador=trabajador,
                    id_Jefe_Departamento=jefe_departamento,
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
    #funciones para editar la solicitud
    def cargar_Formulario_Editar(request, idFormulario):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idFormulario)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)

        # Obtener los valores necesarios para inicializar el formulario
        departamento = solicitud.area_solicitante
        nombre_jefe_departamento = solicitud.responsable_Area
        tipo_servicio_id = solicitud.tipo_servicio
        descripcion = solicitud.descripcion
        fecha=solicitud.fecha
        folio=solicitud.folio
        # Crear un formulario con los datos de la solicitud
        form = SolicitudMantenimientoForm(initial={
            'area_solicitante': departamento,
            'responsable_Area': nombre_jefe_departamento,
            'tipo_servicio': tipo_servicio_id,
            'descripcion': descripcion,
            'fecha': fecha,
            'folio': folio
            
        })
        # Pasar idFormulario al contexto de la plantilla
        context = {
            'form': form,
            'idFormulario': idFormulario,  # Pasar el ID de la solicitud al contexto
        }

        return render(request, 'dep_mantenimiento/layout/solicitante/formularioEdit.html', context)
    
    
    
    
    
    
    def edtiarFormulario(request, idFormulario):
        # Obtener la solicitud correspondiente al idFormulario
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idFormulario)
        except Solicitud_Mantenimiento.DoesNotExist:
            # Manejar el caso en que la solicitud no exista
            return HttpResponse("La solicitud no existe", status=404)
        
        # Verificar si el método de solicitud es POST (es decir, se envió un formulario)
        if request.method == 'POST':
            # Crear un formulario con los datos de la solicitud y los datos enviados en la solicitud POST
            form = SolicitudMantenimientoForm(request.POST, initial={
                'folio': solicitud.folio,
                'tipos_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
            })
            # Verificar si el formulario es válido
            if form.is_valid():
                # Guardar los cambios en la solicitud
                solicitud.folio = form.cleaned_data['folio']
                solicitud.tipo_servicio = form.cleaned_data['tipos_servicio']
                solicitud.descripcion = form.cleaned_data['descripcion']
                solicitud.save()
                # Redirigir a alguna página de éxito o cargar la vista de inicio, por ejemplo
                return redirect('inicio')
        else:
            # Si el método de solicitud no es POST, cargar el formulario con los datos de la solicitud
            form = SolicitudMantenimientoForm(initial={
                'folio': solicitud.folio,
                'tipos_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
            })
        
        # Renderizar el formulario
        return render(request, 'dep_mantenimiento/layout/solicitante/formularioEdit.html', {'form': form})
        
####
def eliminar_solicitud(request, solicitud_id):
    try:
        # Obtener la solicitud
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        
        # Ocultar la solicitud en lugar de eliminarla permanentemente
        solicitud.visible = False
        solicitud.save()

        # Guardar en la bitácora
        bitacora(request.user, 'Solicitud de Mantenimiento', 'Eliminar', solicitud_id, Departamento='Mantenimiento')

        # Reiniciar la secuencia de las solicitudes
        # DELETE FROM solicitud_mantenimiento WHERE id = solicitud_id;
        # SELECT setval('solicitud_mantenimiento_id_seq', (SELECT MAX(id) FROM solicitud_mantenimiento));

        return redirect('inicio')
    except Solicitud_Mantenimiento.DoesNotExist:
        return JsonResponse({'error': 'La solicitud no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
 
#vistas Jefe Departamento
class vistas_Jefe_Departamento_cargar_inicio(View):
    @staticmethod
    def cargar_Inicio(request, id):
        # Lógica para determinar el tipo de usuario
        es_Jeje_dep = True  # Por ejemplo, asumamos que el usuario es un docente

        if es_Jeje_dep:
            
            url_inicio = reverse('inicio_jefe_departamento', args=[id])  # Asegúrate de pasar el id adecuado aquí
        else:
            url_inicio = reverse('inicio')

        contexto = {
            'id': id,
            'url_inicio': url_inicio
        }

        return render(request, 'dep_mantenimiento/layout/jDep/home.html', contexto)
    @staticmethod
    def cargar_Formulario(request, id_Jefe_Departamento):
        # Lógica para determinar el tipo de usuario
        es_Jeje_dep = True  # Por ejemplo, asumamos que el usuario es un docente

        # Obtener la fecha actual
        fecha_actual = datetime.now().date()
        trabajador = trabajadores.objects.get(id=id_Jefe_Departamento)
        # Obtener el área solicitante y el responsable del área
        departamento = trabajador.departamento
        nombre_jefe_departamento = trabajador.nombre_completo()           
               

        # Crear una instancia del formulario con los valores iniciales
        form = SolicitudMantenimientoForm(initial={
            'fecha': fecha_actual,
            'area_solicitante': departamento,
            'responsable_Area': nombre_jefe_departamento,
        })

        if es_Jeje_dep:
            url_formulario = reverse('formulario_jefe_departamento', args=[id_Jefe_Departamento])  # Asegúrate de pasar el id adecuado aquí
        else:
            url_formulario = reverse('inicio')

        contexto = {
            'id': id_Jefe_Departamento,
            'url_formulario': url_formulario,
            'form': form,  # Pasar el formulario al contexto
        }
        return render(request, 'dep_mantenimiento/layout/jdep/formulario.html', contexto)

    @staticmethod
    def obtener_solicitudes(request, id_Jefe):
        try:
            # Filtrar las solicitudes asociadas al jefe de departamento
            solicitudes = Solicitud_Mantenimiento.objects.filter(id_Jefe_Departamento=id_Jefe).order_by('-fecha', '-hora')
            # Obtener la fecha y hora actual
            now = datetime.now()
            # Crear un diccionario para almacenar los datos de las solicitudes
            # Crear una lista para almacenar las solicitudes con la información de los trabajadores
            solicitudes_con_info_trabajador = []

            # Iterar sobre cada solicitud
            for solicitud in solicitudes:
                 # Calcular el tiempo transcurrido
                tiempo_transcurrido = now - datetime.combine(solicitud.fecha, solicitud.hora)
                    # Convertir el tiempo transcurrido a segundos
                tiempo_transcurrido_segundos = tiempo_transcurrido.total_seconds()
                    # Añadir el tiempo transcurrido como un nuevo campo al diccionario de la solicitud
                # Crear un diccionario para almacenar la información de la solicitud
                solicitud_dict = {
                    'id': solicitud.id,
                    'tipo_servicio': solicitud.tipo_servicio,
                    'descripcion': solicitud.descripcion,
                    'status': solicitud.status,
                    'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                    'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                    'tiempo_transcurrido': tiempo_transcurrido_segundos, # Añadir el tiempo transcurrido en segundos
                    'firmado_jefe_departamento': solicitud.firma_Jefe_Departamento,  # Agregar la firma del jefe de departamento
                    'firmado_jefe_mantenimiento': solicitud.firma_Jefe_Mantenimiento,  # Agregar la firma del jefe de mantenimiento
                }

                # Verificar si la solicitud tiene un trabajador asociado
                if solicitud.id_Trabajador:
                    # Obtener la instancia de trabajador asociado a la solicitud
                    trabajador = solicitud.id_Trabajador
                    # Obtener el nombre completo del trabajador utilizando el método nombre_completo del modelo trabajadores
                    nombre_completo = trabajador.nombre_completo()
                    # Agregar el nombre completo del trabajador al diccionario de la solicitud
                    solicitud_dict['nombre_completo_trabajador'] = nombre_completo

                # Agregar el diccionario de la solicitud a la lista de solicitudes con información del trabajador
                solicitudes_con_info_trabajador.append(solicitud_dict)

            # Retornar las solicitudes en formato JSON
            return JsonResponse({'solicitudes': solicitudes_con_info_trabajador})

        except Solicitud_Mantenimiento.DoesNotExist:
            # Si no se encuentran solicitudes, lanzar una excepción Http404
            raise Http404("Las solicitudes del jefe de departamento no existen")

        
    @staticmethod   
    def guardar_datos_Jdep(request, id_Jefe_Departamento):
        if request.method == 'POST':
            form = SolicitudMantenimientoForm(request.POST)
            if form.is_valid():
                id_fecha = datetime.now().date()
                id_folio = form.cleaned_data['folio']
                id_tipos_servicio = form.cleaned_data['tipos_servicio']
                id_descripcion = form.cleaned_data['descripcion']
                hora_actual = datetime.now().time()
                # Obtener la instancia del trabajador correspondiente al ID
                jefe_departamento = trabajadores.objects.get(id=id_Jefe_Departamento)
                departamento = jefe_departamento.departamento
                
                
                nombre_jefe_departamento = jefe_departamento.nombre_completo()
               
               
                # Crea una instancia del modelo Solicitud y asigna los valores
                datos_nuevos = Solicitud_Mantenimiento(
                    fecha=id_fecha,
                    folio=id_folio,
                    area_solicitante=departamento,
                    responsable_Area=nombre_jefe_departamento,  # Aquí asignamos el jefe del departamento como responsable del área
                    tipo_servicio=id_tipos_servicio,
                    descripcion=id_descripcion,
                    hora=hora_actual,                  
                    id_Jefe_Departamento=jefe_departamento,
                    status='Enviado',
                    firma_Jefe_Departamento=True,
                
                )
                
               # Guarda la imagen de firma si está presente en el formulario
            if 'firma_Jefe_Departamento_img' in request.FILES:
                datos_nuevos.firma_Jefe_Departamento_img = request.FILES['firma_Jefe_Departamento_img']
                # Asegúrate de que 'datos_nuevos' sea el objeto que creaste para la solicitud de mantenimiento

            datos_nuevos.save()  # Guarda los datos en la base de datos

            # Redirige a la URL de la vista de inicio del jefe de departamento
            return redirect('inicio_jefe_departamento', id=id_Jefe_Departamento)
        else:
            form = SolicitudMantenimientoForm()
            
        # Renderiza el formulario
        return render(request, 'dep_mantenimiento/layout/jdep/formulario.html', {'form': form})







# Vistas para la sección de Empleados
class vistas_Empleados(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/empleado/home.html', {'id': id})

    @staticmethod
    def obtener_solicitudes(request, idEmpleado):
        try:
            # Filtrar las solicitudes asociadas al empleado
            solicitudes = Solicitud_Mantenimiento.objects.filter(id_Empleado=idEmpleado).order_by('-fecha', '-hora')
            
            # Crear una lista para almacenar las solicitudes con la información adicional
            solicitudes_con_info_adicional = []

            # Iterar sobre cada solicitud
            for solicitud in solicitudes:
                # Crear un diccionario para almacenar la información de la solicitud
                solicitud_dict = {
                    'id': solicitud.id,
                    'tipo_servicio': solicitud.tipo_servicio,
                    'descripcion': solicitud.descripcion,
                    'status': solicitud.status,
                    'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                    'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                    'firmado_jefe_departamento': solicitud.firma_Jefe_Departamento,  # Firma del jefe de departamento
                    'fimrado_empleado': solicitud.firma_Empleado,  # Firma del jefe de mantenimiento
                }

                # Verificar si la solicitud tiene un trabajador asociado
                if solicitud.id_Trabajador:
                    # Obtener la instancia del trabajador asociado a la solicitud
                    trabajador = solicitud.id_Trabajador
                    # Obtener el nombre completo del trabajador utilizando el método nombre_completo del modelo Trabajador
                    nombre_completo = trabajador.nombre_completo()
                    # Obtener el departamento del trabajador
                    departamento = trabajador.departamento
                    # Agregar el nombre completo y el departamento del trabajador al diccionario de la solicitud
                    solicitud_dict['nombre_completo_trabajador'] = nombre_completo
                    solicitud_dict['departamento_trabajador'] = departamento
                elif solicitud.id_Jefe_Departamento:
                    # Obtener la instancia del jefe de departamento asociado a la solicitud
                    jefe_departamento = solicitud.id_Jefe_Departamento
                    # Obtener el nombre completo del jefe de departamento utilizando el método nombre_completo del modelo JefeDepartamento
                    nombre_completo = jefe_departamento.nombre_completo()
                    # Obtener el departamento del jefe de departamento
                    departamento = jefe_departamento.departamento
                    # Agregar el nombre completo y el departamento del jefe de departamento al diccionario de la solicitud
                    solicitud_dict['nombre_completo_jefe_departamento'] = nombre_completo
                    solicitud_dict['departamento_jefe_departamento'] = departamento
                elif solicitud.id_Subdirectora:
                    # Obtener la instancia de la subdirectora asociada a la solicitud
                    subdirectora = solicitud.id_Subdirectora
                    # Obtener el nombre completo de la subdirectora utilizando el método nombre_completo del modelo Subdirectora
                    nombre_completo = subdirectora.nombre_completo()
                    # Obtener el departamento de la subdirectora
                    departamento = subdirectora.departamento
                    # Agregar el nombre completo y el departamento del jefe de departamento al diccionario de la solicitud
                    solicitud_dict['nombre_completo_subdirectora'] = nombre_completo
                    solicitud_dict['departamento_subdirectora'] = departamento
                    
                # Agregar el diccionario de la solicitud a la lista de solicitudes con información adicional
                solicitudes_con_info_adicional.append(solicitud_dict)
            
            # Retornar las solicitudes en formato JSON
            return JsonResponse({'solicitudes': solicitudes_con_info_adicional})
        
        except Solicitud_Mantenimiento.DoesNotExist:
            # Si no se encuentran solicitudes, lanzar una excepción Http404
            raise Http404("Las solicitudes del empleado no existen")

    
# Vistas para la sección de Subdirectora    
class vistas_Subdirectora(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/subdirectora/home.html', {'id': id})   
    @staticmethod
    def obtener_solicitudes(request, idSubdirectora):
        try:
            # Filtrar las solicitudes asociadas al subdirectora
            solicitudes = Solicitud_Mantenimiento.objects.filter(id_Subdirectora=idSubdirectora).order_by('-fecha', '-hora')

            # Crear una lista para almacenar las solicitudes con la información adicional   
            solicitudes_con_info_adicional = []
            # Obtener la fecha y hora actual
            now = datetime.now()
            # Iterar sobre cada solicitud
            for solicitud in solicitudes:
                 # Calcular el tiempo transcurrido
                tiempo_transcurrido = now - datetime.combine(solicitud.fecha, solicitud.hora)
                    # Convertir el tiempo transcurrido a segundos
                tiempo_transcurrido_segundos = tiempo_transcurrido.total_seconds()
                # Crear un diccionario para almacenar la información de la solicitud
                solicitud_dict = {
                    'id': solicitud.id,
                    'tipo_servicio': solicitud.tipo_servicio,
                    'descripcion': solicitud.descripcion,
                    'status': solicitud.status,
                    'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                    'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                    'firmado_jefe_departamento': solicitud.firma_Jefe_Departamento,  # Firma del jefe de departamento
                    'resolvio':solicitud.resolvio,
                    'tiempo_transcurrido': tiempo_transcurrido
                }
                 # Verificar si la solicitud tiene un trabajador asociado
                if solicitud.id_Trabajador:
                    # Obtener la instancia del trabajador asociado a la solicitud
                    trabajador = solicitud.id_Trabajador
                    # Obtener el nombre completo del trabajador utilizando el método nombre_completo del modelo Trabajador
                    nombre_completo = trabajador.nombre_completo()
                    # Obtener el departamento del trabajador
                    departamento = trabajador.departamento
                    # Agregar el nombre completo y el departamento del trabajador al diccionario de la solicitud
                    solicitud_dict['nombre_completo_trabajador'] = nombre_completo
                    solicitud_dict['departamento_trabajador'] = departamento
                elif solicitud.id_Jefe_Departamento:
                    # Obtener la instancia del jefe de departamento asociado a la solicitud
                    jefe_departamento = solicitud.id_Jefe_Departamento
                    # Obtener el nombre completo del jefe de departamento utilizando el método nombre_completo del modelo JefeDepartamento
                    nombre_completo = jefe_departamento.nombre_completo()
                    # Obtener el departamento del jefe de departamento
                    departamento = jefe_departamento.departamento
                    # Agregar el nombre completo y el departamento del jefe de departamento al diccionario de la solicitud
                    solicitud_dict['nombre_completo_jefe_departamento'] = nombre_completo
                    solicitud_dict['departamento_jefe_departamento'] = departamento
                    
                
                # Agregar el diccionario de la solicitud a la lista de solicitudes con información adicional
                solicitudes_con_info_adicional.append(solicitud_dict)
            
            # Retornar las solicitudes en formato JSON
            return JsonResponse({'solicitudes': solicitudes_con_info_adicional})
        
        except Solicitud_Mantenimiento.DoesNotExist:
            # Si no se encuentran solicitudes, lanzar una excepción Http404
            raise Http404("Las solicitudes del subdirectora no existen")

#vistas para el jefe de Mantenimiento
class vistas_Jefe_Mantenimiento(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/jMantenimiento/home.html', {'id': id})
   
    @staticmethod
    def obtener_solicitudes(request, idJefeMantenimiento):
        try:
            # Filtrar las solicitudes asociadas al empleado
            solicitudes = Solicitud_Mantenimiento.objects.filter(id_Jefe_Mantenimiento=idJefeMantenimiento).order_by('-fecha', '-hora')
            
            # Crear una lista para almacenar las solicitudes con la información adicional
            solicitudes_con_info_adicional = []

            # Iterar sobre cada solicitud
            for solicitud in solicitudes:
                # Crear un diccionario para almacenar la información de la solicitud
                solicitud_dict = {
                    'id': solicitud.id,
                    'tipo_servicio': solicitud.tipo_servicio,
                    'descripcion': solicitud.descripcion,
                    'status': solicitud.status,
                    'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                    'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                    'firmado_jefe_departamento': solicitud.firma_Jefe_Departamento,  # Firma del jefe de departamento
                    'fimrado_empleado': solicitud.firma_Empleado,  # Firma del jefe de mantenimiento
                }

                # Verificar si la solicitud tiene un trabajador asociado
                if solicitud.id_Trabajador:
                    # Obtener la instancia del trabajador asociado a la solicitud
                    trabajador = solicitud.id_Trabajador
                    # Obtener el nombre completo del trabajador utilizando el método nombre_completo del modelo Trabajador
                    nombre_completo = trabajador.nombre_completo()
                    # Obtener el departamento del trabajador
                    departamento = trabajador.departamento
                    # Agregar el nombre completo y el departamento del trabajador al diccionario de la solicitud
                    solicitud_dict['nombre_completo_trabajador'] = nombre_completo
                    solicitud_dict['departamento_trabajador'] = departamento
                elif solicitud.id_Jefe_Departamento:
                    # Obtener la instancia del jefe de departamento asociado a la solicitud
                    jefe_departamento = solicitud.id_Jefe_Departamento
                    # Obtener el nombre completo del jefe de departamento utilizando el método nombre_completo del modelo JefeDepartamento
                    nombre_completo = jefe_departamento.nombre_completo()
                    # Obtener el departamento del jefe de departamento
                    departamento = jefe_departamento.departamento
                    # Agregar el nombre completo y el departamento del jefe de departamento al diccionario de la solicitud
                    solicitud_dict['nombre_completo_jefe_departamento'] = nombre_completo
                    solicitud_dict['departamento_jefe_departamento'] = departamento
                elif solicitud.id_Subdirectora:
                    # Obtener la instancia de la subdirectora asociada a la solicitud
                    subdirectora = solicitud.id_Subdirectora
                    # Obtener el nombre completo de la subdirectora utilizando el método nombre_completo del modelo Subdirectora
                    nombre_completo = subdirectora.nombre_completo()
                    # Obtener el departamento de la subdirectora
                    departamento = subdirectora.departamento
                    # Agregar el nombre completo y el departamento del jefe de departamento al diccionario de la solicitud
                    solicitud_dict['nombre_completo_subdirectora'] = nombre_completo
                    solicitud_dict['departamento_subdirectora'] = departamento
                if solicitud.id_Empleado:
                    # Obtener la instancia del empleado asociado a la solicitud
                    empleado = solicitud.id_Empleado
                    # Obtener el departamento del empleado
                    departamento = empleado.departamento
                    # Verificar si el departamento del empleado coincide con el departamento de mantenimiento
                    if departamento == 'Mantenimiento de Equipo':
                        # Si coincide, procede a agregar la información al diccionario de la solicitud
                        nombre_completo = empleado.nombre_completo()
                        solicitud_dict['nombre_completo_empleado'] = nombre_completo
                        solicitud_dict['departamento_empleado'] = departamento
                    
                # Agregar el diccionario de la solicitud a la lista de solicitudes con información adicional
                solicitudes_con_info_adicional.append(solicitud_dict)
            
            # Retornar las solicitudes en formato JSON
            return JsonResponse({'solicitudes': solicitudes_con_info_adicional})
        
        except Solicitud_Mantenimiento.DoesNotExist:
            # Si no se encuentran solicitudes, lanzar una excepción Http404
            raise Http404("Las solicitudes del jefe de mantenimiento no existen")
        


    
    

class Error404Views(TemplateView):
    template_name="404.html"



class Error403Views(TemplateView):
    template_name="403.html"



#@perssion  
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



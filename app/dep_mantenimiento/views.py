from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse,Http404,HttpResponseForbidden
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
from .models import HistorialSolicitud, Solicitud_Mantenimiento, imagenesEvidencias,trabajadores
from django.shortcuts import redirect

from .forms import Evidencias, Peticionform, Rechazarform, Solcitud_confirmacion, SolicitudAsignar, SolicitudMantenimientoForm, SolicitudPeticion, firma_Formulario_Empleado, firmaVoBoForm, firmar_Formulario
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
            # Verificar si el trabajador pertenece al grupo "Subdirectora de Servicios Administrativos"
            elif trabajador.grupos.filter(name='Subdirectora de Servicios Administrativos').exists():
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

def Solicitante_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el objeto trabajador asociado al usuario actual
            try:
                trabajador = trabajadores.objects.get(user_id=request.user.id)
            except trabajadores.DoesNotExist:
                raise PermissionDenied  # Si no se encuentra el trabajador, denegar el acceso

            # Verificar si el trabajador pertenece al grupo 'Solicitante'
            if trabajador.grupos.filter(name='Solicitante').exists():
                return view_func(request, *args, **kwargs)
        
        # Si el usuario no pertenece al grupo 'Solicitante', mostrar la página de error 403
        raise PermissionDenied
    
    return wrapper

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
                        'tiempo_transcurrido': tiempo_transcurrido_segundos, # Añadir el tiempo transcurrido en segundos
                        'ocultar': solicitud.ocultar,
                        'firma_Jefe_Departamento': solicitud.firma_Jefe_Departamento,  # Agregar la firma del jefe de departamento
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
                id_tipos_servicio = form.cleaned_data['tipo_servicio']
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
                bitacora(request.user, 'Solicitud_Mantenimiento', 'add', f'Folio: {id_folio}',Departamento='dep_mantenimiento')

                # Guarda los datos en la base de datos
                datos_nuevos.save()

                # Redirige a la URL de la vista de inicio del docente
                return redirect('inicio_docente', id=id_Docente)
        else:
            form = SolicitudMantenimientoForm()
            
        # Renderiza el formulario
        return render(request, 'dep_mantenimiento/layout/solicitante/formulario.html', {'form': form})
    
    
    
    
    
    
    
    def cargar_Formulario_Editar(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)      
        if request.method == 'POST':
            form = Solcitud_confirmacion(request.POST)
            
            solicitud.descripcion = request.POST.get('descripcion')
            solicitud.tipo_servicio = request.POST.get('tipo_servicio')
            solicitud.save()
            return redirect('inicio')
        else:
            form= Solcitud_confirmacion(initial={
                'area_solicitante': solicitud.area_solicitante,
                'responsable_Area': solicitud.responsable_Area,
                'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                'tipo_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
                'folio': solicitud.folio,
            })
            
            context = {
                'solicitud': solicitud,
                'id': idSolicitud,
                'form':form
            }
            return render(request, 'dep_mantenimiento/layout/solicitante/formularioEdit.html', context)
   
    def cargar_Solicitud(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id).order_by('-fecha', '-hora').first()
        
        fecha_histo = historial.fecha.strftime("%d-%m-%Y") if historial else None
        hora_histo = historial.hora.strftime("%H:%M") if historial else None

        context = {
            'solicitud': solicitud,
            'id': solicitud_id,
            'fecha': solicitud.fecha.strftime("%d/%m/%Y"),
            'hora': solicitud.hora.strftime("%H:%M"),
            'fecha_histo': fecha_histo,
            'hora_histo': hora_histo,
        }
        
        return render(request, 'dep_mantenimiento/layout/solicitante/solicitudDetallada.html', context)
    
    
        
####
def eliminar_solicitud(request, solicitud_id):
    try:
        # Obtener la solicitud
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        
        # Ocultar la solicitud en lugar de eliminarla permanentemente
        solicitud.ocultar = True
        solicitud.save()
     
        # Guardar en la bitácora
        bitacora(request.user, 'Solicitud_Mantenimiento', 'delete', f'Solicitud eliminada: {solicitud_id}',Departamento='dep_mantenimiento')

        # Reiniciar la secuencia de las solicitudes
        # DELETE FROM solicitud_mantenimiento WHERE id = solicitud_id;
        # SELECT setval('solicitud_mantenimiento_id_seq', (SELECT MAX(id) FROM solicitud_mantenimiento));

        return redirect('inicio')
    except Solicitud_Mantenimiento.DoesNotExist:
        return JsonResponse({'error': 'La solicitud no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def JefeDep_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el objeto trabajador asociado al usuario actual
            try:
                trabajador = trabajadores.objects.get(user_id=request.user.id)
            except trabajadores.DoesNotExist:
                raise PermissionDenied  # Si no se encuentra el trabajador, denegar el acceso

            # Verificar si el trabajador pertenece al grupo 'Jefe Departamento'
            if trabajador.grupos.filter(name='Jefe Departamento').exists():
                return view_func(request, *args, **kwargs)
        
        # Si el usuario no está autenticado o no pertenece al grupo 'Jefe Departamento',
        # retornar una respuesta HTTP Forbidden
        return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    return wrapper
    
 
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
    def cargar_Formulario(request, id_JefeDepartamento):
        if request.method == 'POST':
            form = Solcitud_confirmacion(request.POST, request.FILES)
            if form.is_valid():
                # Guardar los datos del formulario
                id_fecha = datetime.now().date()
                id_hora= datetime.now().time()
                id_folio = form.cleaned_data['folio']
                id_tipos_servicio = form.cleaned_data['tipo_servicio']
                id_descripcion = form.cleaned_data['descripcion']
                # Obtener la instancia del trabajador correspondiente al ID
                trabajador = trabajadores.objects.get(id=id_JefeDepartamento)
                id_departamento = trabajador.departamento
                id_nombre = trabajador.nombre_completo()
                # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                id_firma_jefe_departamentoimg = form.cleaned_data['firma_Jefe_Departamento_img']
                # Obtener solo el ID del jefe del departamento de Mantenimiento de Equipo
                jefe_departamentoMAnt = trabajadores.objects.filter(departamento='Mantenimiento de Equipo', puesto='Jefe').values('id').first()
                        
                # Obtener la instancia del jefe del departamento de Mantenimiento de Equipo
                jefe_departamento_instance = trabajadores.objects.get(id=jefe_departamentoMAnt['id'])
        
                        
                datos_nuevos = Solicitud_Mantenimiento(
                    fecha=id_fecha,
                    folio=id_folio,
                    area_solicitante=id_departamento,
                    responsable_Area=id_nombre,  # Aquí asignamos el jefe del departamento como responsable del área
                    tipo_servicio=id_tipos_servicio,
                    descripcion=id_descripcion,
                    hora=id_hora,
                    id_Jefe_Departamento=trabajador,
                    status='Enviado',
                    firma_Jefe_Departamento_img=id_firma_jefe_departamentoimg,
                    id_Jefe_Mantenimiento=jefe_departamento_instance,
                    firma_Jefe_Departamento=True
                )
                bitacora(request.user, 'Solicitud_Mantenimiento', 'add', f'Folio: {id_folio}', Departamento='dep_mantenimiento')
                datos_nuevos.save()
                return redirect('inicio_jefe_departamento', id=id_JefeDepartamento)
        else:
            # La solicitud no es un POST, renderiza el formulario vacío
            trabajador = trabajadores.objects.get(id=id_JefeDepartamento)
            departamento = trabajador.departamento
            Nombre = trabajador.nombre_completo()
            fecha = datetime.now().date()
            # Crear un formulario con los datos de la solicitud
            form = Solcitud_confirmacion(initial={
                'area_solicitante': departamento,
                'responsable_Area': Nombre,
                'fecha': fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
            })
            # Pasar idFormulario al contexto de la plantilla
            context = {
                'form': form,
                'id': id_JefeDepartamento,
                    # Pasar el ID de la solicitud al contexto
            }
            return render(request, 'dep_mantenimiento/layout/jDep/formulario.html', context)




    





    @staticmethod
    def firmarFormulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)
        
        
        
        if request.method == 'POST':
            form = firmar_Formulario(request.POST, request.FILES)  # Pasar la instancia de la solicitud existente al formulario
            if form.is_valid():
                 # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                id_firma_jefe_departamentoimg = form.cleaned_data['firma_Jefe_Departamento_img']
                # Obtener solo el ID del jefe del departamento de Mantenimiento de Equipo
                jefe_departamentoMAnt = trabajadores.objects.filter(departamento='Mantenimiento de Equipo', puesto='Jefe').values('id').first()                        
                # Obtener la instancia del jefe del departamento de Mantenimiento de Equipo
                jefe_departamento_instance = trabajadores.objects.get(id=jefe_departamentoMAnt['id'])
                solicitud.firma_Jefe_Departamento_img=id_firma_jefe_departamentoimg
                solicitud.firma_Jefe_Departamento=True
                solicitud.id_Jefe_Mantenimiento=jefe_departamento_instance
                solicitud.save() # Guardar los cambios en la solicitud existente
                bitacora(request.user, 'Solicitud_Mantenimiento', 'Post', f'Solicitud: {idSolicitud}', Departamento='dep_mantenimiento')
                return redirect('inicio')
        else:
            # Pre-rellenar el formulario con los datos existentes
            form = firmar_Formulario(initial={
                'area_solicitante': solicitud.area_solicitante,
                'responsable_Area': solicitud.responsable_Area,
                'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                
                'tipo_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
                'folio': solicitud.folio,
            })
        
        context = {
            'form': form,
            'id': idSolicitud,
            'solicitud': solicitud,  # Incluir la solicitud en el contexto para acceso en la plantilla
        }
        return render(request, 'dep_mantenimiento/layout/jDep/firma_form.html', context)
        
 
    @staticmethod
    def firmarFormularioVoBo(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
            evidencias = imagenesEvidencias.objects.filter(solicitud=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)
        
        if request.method == 'POST':
            form = firmaVoBoForm(request.POST, request.FILES)
            if form.is_valid():
                id_firma_jefe_departamentoVoBoimg = form.cleaned_data['firma_Jefe_VoBo_img']
                solicitud.firma_Jefe_VoBo_img = id_firma_jefe_departamentoVoBoimg
                solicitud.firma_Jefe_VoBo = True
                solicitud.status = 'Realizado'
                solicitud.save()
                bitacora(request.user, 'Solicitud_Mantenimiento', 'Post', f'Solicitud: {idSolicitud}', Departamento='dep_mantenimiento')
                return redirect('inicio')
        else:
            form = firmaVoBoForm()
            empleado = solicitud.id_Empleado
            nombre_completo_empleado = empleado.nombre_completo()
        
        context = {
            'form': form,
            'id': idSolicitud,
            'solicitud': solicitud,
            'empleado': nombre_completo_empleado,
            'evidencias': evidencias
        }
        return render(request, 'dep_mantenimiento/layout/jDep/firma_form_VoBo.html', context)
            
        
    @staticmethod
    def editar_Formulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)      
        if request.method == 'POST':
            form = Solcitud_confirmacion(request.POST)
            
            solicitud.descripcion = request.POST.get('descripcion')
            solicitud.tipo_servicio = request.POST.get('tipo_servicio')
            solicitud.save()
            return redirect('inicio')
        else:
            form= Solcitud_confirmacion(initial={
                'area_solicitante': solicitud.area_solicitante,
                'responsable_Area': solicitud.responsable_Area,
                 'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                'tipo_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
                'folio': solicitud.folio,
            })
            
            context = {
                'solicitud': solicitud,
                'id': idSolicitud,
                'form':form
            }
            return render(request, 'dep_mantenimiento/layout/jDep/formularioedit.html', context)
                 
        
        
        

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
                    'ocultar': solicitud.ocultar,
                    'firmaEmpleados': solicitud.firma_Empleado,
                    'firmaVobo':solicitud.firma_Jefe_VoBo
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
        
    def cargar_Solicitud(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id).order_by('-fecha', '-hora').first()
        
        fecha_histo = historial.fecha.strftime("%d-%m-%Y") if historial else None
        hora_histo = historial.hora.strftime("%H:%M") if historial else None

        context = {
            'solicitud': solicitud,
            'id': solicitud_id,
            'fecha': solicitud.fecha.strftime("%d/%m/%Y"),
            'hora': solicitud.hora.strftime("%H:%M"),
            'fecha_histo': fecha_histo,
            'hora_histo': hora_histo,
        }
        
        return render(request, 'dep_mantenimiento/layout/jDep/solicitudDetallada.html', context)    

        




def Empleado_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el objeto trabajador asociado al usuario actual
            try:
                trabajador = trabajadores.objects.get(user_id=request.user.id)
            except trabajadores.DoesNotExist:
                raise PermissionDenied  # Si no se encuentra el trabajador, denegar el acceso

            # Verificar si el trabajador pertenece al grupo 'Empleado de Mantenimiento de Equipo'
            if trabajador.grupos.filter(name='Empleado de Mantenimiento de Equipo').exists():
                return view_func(request, *args, **kwargs)
        
        # Si el usuario no pertenece al grupo 'Empleado de Mantenimiento de Equipo', mostrar la página de error 403
        raise PermissionDenied
    
    return wrapper



# Vistas para la sección de Empleados
class vistas_Empleados(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/empleado/home.html', {'id': id})

    @staticmethod
    def firmarFormulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)

        if request.method == 'POST':
            form = firma_Formulario_Empleado(request.POST, request.FILES)
            form1=Evidencias(request.POST, request.FILES)
            if form.is_valid() and form1.is_valid():
                solicitud.firma_Empleado_img = form.cleaned_data['firma_Empleado_img']
                solicitud.material_utilizado = form.cleaned_data['material_utilizado']
                solicitud.des_Serv_Realizado = form.cleaned_data['des_Serv_Realizado']

                # Guardar las imágenes múltiples en el campo evidenciasIMG
                images = request.FILES.getlist('evidenciasIMG')
                evi=form1.save(commit=False)
                for image in images:
                   
                     evi = imagenesEvidencias(
                        solicitud=solicitud,
                        evidenciasIMG=image,     
                     )
                     evi.save()
                    
                
                solicitud.status = 'Solicitud_Firmada'
                solicitud.firma_Empleado = True
                solicitud.save()
                
                return redirect('inicio')
            
            
        else:
            form = firma_Formulario_Empleado()
            empleado = trabajadores.objects.get(id=solicitud.id_Empleado.id)
            # Obtener el empleado asociado a la solicitud
            empleado = trabajadores.objects.get(id=solicitud.id_Empleado.id)
            # Obtener el nombre completo del empleado
            nombre_completo_empleado = empleado.nombre_completo()
        context = {
            'solicitud': solicitud,
            'id': idSolicitud,
            'form': form,
            'empleado':nombre_completo_empleado
        }
        return render(request, 'dep_mantenimiento/layout/empleado/firma_form.html', context)
                    
    def cargar_Solicitud(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id).order_by('-fecha', '-hora').first()
        
        fecha_histo = historial.fecha.strftime("%d-%m-%Y") if historial else None
        hora_histo = historial.hora.strftime("%H:%M") if historial else None

        context = {
            'solicitud': solicitud,
            'id': solicitud_id,
            'fecha': solicitud.fecha.strftime("%d/%m/%Y"),
            'hora': solicitud.hora.strftime("%H:%M"),
            'fecha_histo': fecha_histo,
            'hora_histo': hora_histo,
        }
        
        return render(request, 'dep_mantenimiento/layout/empleado/solicitudDetallada.html', context)         
         
         
                

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

def Sub_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el objeto trabajador asociado al usuario actual
            try:
                trabajador = trabajadores.objects.get(user_id=request.user.id)
            except trabajadores.DoesNotExist:
                raise PermissionDenied  # Si no se encuentra el trabajador, denegar el acceso

            # Verificar si el trabajador pertenece al grupo 'Subdirectora de Servicios Administrativos'
            if trabajador.grupos.filter(name='Subdirectora de Servicios Administrativos').exists():
                return view_func(request, *args, **kwargs)
        
        # Si el usuario no pertenece al grupo 'Subdirectora de Servicios Administrativos', mostrar la página de error 403
        raise PermissionDenied
    
    return wrapper


    
# Vistas para la sección de Subdirectora    
class vistas_Subdirectora(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/subdirectora/home.html', {'id': id})
       
    @staticmethod
    def cargar_Formulario(request, idSubdirectora):
        if request.method == 'POST':
            form = Solcitud_confirmacion(request.POST, request.FILES)
            if form.is_valid():
                # Guardar los datos del formulario
                id_fecha = datetime.now().date()
                id_hora= datetime.now().time()
                id_folio = form.cleaned_data['folio']
                id_tipos_servicio = form.cleaned_data['tipo_servicio']
                id_descripcion = form.cleaned_data['descripcion']
                # Obtener la instancia del trabajador correspondiente al ID
                trabajador = trabajadores.objects.get(id=idSubdirectora)
                id_departamento = trabajador.departamento
                id_nombre = trabajador.nombre_completo()
                # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                id_firma_jefe_departamentoimg = form.cleaned_data['firma_Jefe_Departamento_img']
                # Obtener solo el ID del jefe del departamento de Mantenimiento de Equipo
                jefe_departamentoMAnt = trabajadores.objects.filter(departamento='Mantenimiento de Equipo', puesto='Jefe').values('id').first()                        
                # Obtener la instancia del jefe del departamento de Mantenimiento de Equipo
                jefe_departamento_instance = trabajadores.objects.get(id=jefe_departamentoMAnt['id'])
        
                        
                datos_nuevos = Solicitud_Mantenimiento(
                    fecha=id_fecha,
                    folio=id_folio,
                    area_solicitante=id_departamento,
                    responsable_Area=id_nombre,  # Aquí asignamos el jefe del departamento como responsable del área
                    tipo_servicio=id_tipos_servicio,
                    descripcion=id_descripcion,
                    hora=id_hora,
                    id_Subdirectora=trabajador,
                    status='Enviado',
                    firma_Jefe_Departamento_img=id_firma_jefe_departamentoimg,
                    id_Jefe_Mantenimiento=jefe_departamento_instance,
                    firma_Jefe_Departamento=True
                )
                bitacora(request.user, 'Solicitud_Mantenimiento', 'add', f'Folio: {id_folio}', Departamento='dep_mantenimiento')
                datos_nuevos.save()
                return redirect('inicio_subdirector_servicios', id=idSubdirectora)
        else:
            # La solicitud no es un POST, renderiza el formulario vacío
            trabajador = trabajadores.objects.get(id=idSubdirectora)
            departamento = trabajador.departamento
            Nombre = trabajador.nombre_completo()
            fecha = datetime.now().date()
            # Crear un formulario con los datos de la solicitud
            form = Solcitud_confirmacion(initial={
                'area_solicitante': departamento,
                'responsable_Area': Nombre,
                'fecha': fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
            })
            # Pasar idFormulario al contexto de la plantilla
            context = {
                'form': form,
                'id': idSubdirectora,
                    # Pasar el ID de la solicitud al contexto
            }
            return render(request, 'dep_mantenimiento/layout/subdirectora/formulario.html', context)
       
       
    @staticmethod
    def editar_Formulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)      
        if request.method == 'POST':
            form = Solcitud_confirmacion(request.POST)
            
            solicitud.descripcion = request.POST.get('descripcion')
            solicitud.tipo_servicio = request.POST.get('tipo_servicio')
            solicitud.save()
            return redirect('inicio')
        else:
            form= Solcitud_confirmacion(initial={
                'area_solicitante': solicitud.area_solicitante,
                'responsable_Area': solicitud.responsable_Area,
                 'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                'tipo_servicio': solicitud.tipo_servicio,
                'descripcion': solicitud.descripcion,
                'folio': solicitud.folio,
            })
            
            context = {
                'solicitud': solicitud,
                'id': idSolicitud,
                'form':form
            }
            return render(request, 'dep_mantenimiento/layout/subdirectora/formularioedit.html', context)



    @staticmethod
    def peticion_formulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)      
        if request.method == 'POST':
            form = SolicitudPeticion(request.POST)
            
            # Si hay una descripción de rechazo, cambiar el estatus a rechazado
            if request.POST.get('Mat_Rechazo'):
                    solicitud.Mat_Rechazo = request.POST.get('Mat_Rechazo')
                    solicitud.status = 'Rechazado'
                    solicitud.resolvio = False
                # Si hay una descripción de resuelto, cambiar el estatus a Enviado
            elif request.POST.get('Mat_Resuelto'):
                    solicitud.Mat_Resuelto = request.POST.get('Mat_Resuelto')
                    solicitud.status = 'Enviado'
                    solicitud.resolvio = True
              
              
            solicitud.save()
            return redirect('inicio')
        else:
            form= SolicitudPeticion()
            
            context = {
                'solicitud': solicitud,
                'id': idSolicitud,
                'form':form
            }
            return render(request, 'dep_mantenimiento/layout/subdirectora/peticion_form.html', context)



    @staticmethod
    def firmarFormularioVoBo(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
            evidencias = imagenesEvidencias.objects.filter(solicitud=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)
        
        
        
        if request.method == 'POST':
            form = firmaVoBoForm(request.POST, request.FILES)  # Pasar la instancia de la solicitud existente al formulario
            if form.is_valid():
                 # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                id_firma_jefe_departamentoVoBoimg = form.cleaned_data['firma_Jefe_VoBo_img']
                
                        
                # Obtener la instancia del jefe del departamento de Mantenimiento de Equipo
                
                solicitud.firma_Jefe_VoBo_img=id_firma_jefe_departamentoVoBoimg
                solicitud.firma_Jefe_VoBo=True
                solicitud.status = 'Realizado'
                solicitud.save() # Guardar los cambios en la solicitud existente
                bitacora(request.user, 'Solicitud_Mantenimiento', 'Post', f'Solicitud: {idSolicitud}', Departamento='dep_mantenimiento')
                return redirect('inicio')
        else:
            # Pre-rellenar el formulario con los datos existentes
            form = firmaVoBoForm()
            empleado = trabajadores.objects.get(id=solicitud.id_Empleado.id)
            # Obtener el empleado asociado a la solicitud
            empleado = trabajadores.objects.get(id=solicitud.id_Empleado.id)
            # Obtener el nombre completo del empleado
            nombre_completo_empleado = empleado.nombre_completo()
        context = {
            'form': form,
            'id': idSolicitud,
            'solicitud': solicitud,  # Incluir la solicitud en el contexto para acceso en la plantilla
            'empleado': nombre_completo_empleado,
            'evidencias': evidencias
        }
        return render(request, 'dep_mantenimiento/layout/subdirectora/firma_form_VoBo.html', context)

    def cargar_Solicitud(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id).order_by('-fecha', '-hora').first()
        
        fecha_histo = historial.fecha.strftime("%d-%m-%Y") if historial else None
        hora_histo = historial.hora.strftime("%H:%M") if historial else None

        context = {
            'solicitud': solicitud,
            'id': solicitud_id,
            'fecha': solicitud.fecha.strftime("%d/%m/%Y"),
            'hora': solicitud.hora.strftime("%H:%M"),
            'fecha_histo': fecha_histo,
            'hora_histo': hora_histo,
        }
        
        return render(request, 'dep_mantenimiento/layout/subdirectora/solicitudDetallada.html', context)









       
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
                solicitud_dict = {'id': solicitud.id,
                    'tipo_servicio': solicitud.tipo_servicio,
                    'descripcion': solicitud.descripcion,
                    'status': solicitud.status,
                    'fecha': solicitud.fecha.strftime("%d/%m/%Y"),  # Formatear la fecha como dd/mm/aaaa
                    'hora': solicitud.hora.strftime("%H:%M"),  # Formatear la hora como hh:mm
                    'tiempo_transcurrido': tiempo_transcurrido_segundos, # Añadir el tiempo transcurrido en segundos
                    'firmado_jefe_departamento': solicitud.firma_Jefe_Departamento,  # Agregar la firma del jefe de departamento
                    'ocultar': solicitud.ocultar,
                    'firmaEmpleados': solicitud.firma_Empleado,
                    'firmaVobo':solicitud.firma_Jefe_VoBo,
                    'resolvio':solicitud.resolvio,
                    'peticcion':solicitud.des_Peticion_Mat,
                    'id_subdirectora':idSubdirectora
                    
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

def JefeMan_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Obtener el objeto trabajador asociado al usuario actual
            try:
                trabajador = trabajadores.objects.get(user_id=request.user.id)
            except trabajadores.DoesNotExist:
                raise PermissionDenied  # Si no se encuentra el trabajador, denegar el acceso

            # Verificar si el trabajador pertenece al grupo 'Jefe de Mantenimiento de Equipos'
            if trabajador.grupos.filter(name='Jefe de Mantenimiento de Equipo').exists():
                return view_func(request, *args, **kwargs)
        
        # Si el usuario no pertenece al grupo 'Jefe de Mantenimiento de Equipos', mostrar la página de error 403
        raise PermissionDenied
    
    return wrapper



#vistas para el jefe de Mantenimiento
class vistas_Jefe_Mantenimiento(View):
    @staticmethod
    def cargar_Inicio(request, id):
        return render(request, 'dep_mantenimiento/layout/jMantenimiento/home.html', {'id': id})
   
    @staticmethod 
    @transaction.atomic
    def guardar_Asignacion(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)

        if request.method == 'POST':
            form = SolicitudAsignar(request.POST, request.FILES)
            if form.is_valid():
                id_idEmpleado = form.cleaned_data['empleado']
                id_materialAsignado = form.cleaned_data['material_Asignado']
                empleado_asignado = trabajadores.objects.get(id=id_idEmpleado)
                solicitud.id_Empleado = empleado_asignado
                solicitud.material_asignado = id_materialAsignado 
                solicitud.status = 'En_proceso'  # Actualizar el status a "En_proceso"
                
                # Verificar si se envió un motivo de rechazo y actualizar el atributo correspondiente
                
                
                solicitud.save()
                bitacora(request.user, 'Solicitud_Mantenimiento', 'add', f'solicitudId: {solicitud_id}', Departamento='dep_mantenimiento')
                return redirect('inicio')
            else:
                print("El formulario no es válido")
                print(form.errors)
                return HttpResponseServerError("Error en el formulario. Por favor, corrija los errores y vuelva a intentarlo.")
        else:
            initial_data = {
                'material_Asignado': solicitud.material_asignado,
                'empleado': solicitud.id_Empleado.id if solicitud.id_Empleado else None,
            }
            form = SolicitudAsignar(initial=initial_data)
    
            if solicitud.id_Empleado:
                form.fields['empleado'].widget.attrs['readonly'] = True

            context = {
                'solicitud': solicitud,
                'id': solicitud_id,
                'form': form
            }
    
            return render(request, 'dep_mantenimiento/layout/jMantenimiento/estatus.html',context)
   
   
    def cargar_Solicitud(request, solicitud_id):
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id).order_by('-fecha', '-hora').first()
        
        fecha_histo = historial.fecha.strftime("%d-%m-%Y") if historial else None
        hora_histo = historial.hora.strftime("%H:%M") if historial else None

        
        if request.method == 'POST':
            form = SolicitudAsignar(request.POST)
            if form.is_valid():
                id_idEmpleado = form.cleaned_data['empleado']
                id_materialAsignado = form.cleaned_data['material_Asignado']
                empleado_asignado = trabajadores.objects.get(id=id_idEmpleado)
                solicitud.id_Empleado = empleado_asignado
                solicitud.material_asignado = id_materialAsignado 
                solicitud.status = 'En_proceso'  # Actualizar el status a "En_proceso"
                
                # Verificar si se envió un motivo de rechazo y actualizar el atributo correspondiente
                
                
                solicitud.save()
                bitacora(request.user, 'Solicitud_Mantenimiento', 'add', f'solicitudId: {solicitud_id}', Departamento='dep_mantenimiento')
                return redirect('inicio')
            else:
                print("El formulario no es válido")
                print(form.errors)
                return HttpResponseServerError("Error en el formulario. Por favor, corrija los errores y vuelva a intentarlo.")
        else:
            initial_data = {
                'material_Asignado': solicitud.material_asignado,
                'empleado': solicitud.id_Empleado.id if solicitud.id_Empleado else None,
            }
            form = SolicitudAsignar(initial=initial_data)
    
            if solicitud.id_Empleado:
                form.fields['empleado'].widget.attrs['readonly'] = True



            context = {
                'solicitud': solicitud,
                'id': solicitud_id,
                'fecha': solicitud.fecha.strftime("%d/%m/%Y"),
                'hora': solicitud.hora.strftime("%H:%M"),
                'fecha_histo': fecha_histo,
                'hora_histo': hora_histo,
                'form': form
            }
        
        return render(request, 'dep_mantenimiento/layout/jMantenimiento/solicitudDetallada.html', context)
   
   
    @staticmethod
    def rechazarFormulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)
        if request.method == 'POST':
            form = Rechazarform(request.POST)  # Pasar la instancia de la solicitud existente al formulario
            if form.is_valid():
                 # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                motv_rechazo = form.cleaned_data['motv_rechazo']
                solicitud.motv_rechazo = motv_rechazo
                solicitud.status = 'Rechazado'
                solicitud.save()
                bitacora(request.user, 'Solicitud_Mantenimiento', 'Post', f'Folio: {solicitud.folio}', Departamento='dep_mantenimiento')
                return redirect('inicio')
        else:
            form = Rechazarform()
            contexto = {'form': form, 'solicitud': solicitud, 'id': idSolicitud,'fecha':solicitud.fecha.strftime("%d/%m/%Y")}
        return render(request, 'dep_mantenimiento/layout/jMantenimiento/rechazar.html', contexto)
    
    @staticmethod
    def peticionFormulario(request, idSolicitud):
        try:
            solicitud = Solicitud_Mantenimiento.objects.get(id=idSolicitud)
        except Solicitud_Mantenimiento.DoesNotExist:
            return HttpResponse("La solicitud no existe", status=404)
        if request.method == 'POST':
            form = Peticionform(request.POST)  # Pasar la instancia de la solicitud existente al formulario
            if form.is_valid():
                 # Guarda la imagen en el campo firma_Jefe_Departamento_img del modelo Solicitud_Mantenimiento
                des_Peticion_Mat = form.cleaned_data['des_Peticion_Mat']
                solicitud.des_Peticion_Mat = des_Peticion_Mat
                solicitud.status = 'En_espera'
                idsubdirectora = trabajadores.objects.filter(departamento='Servicios Administrativos', puesto='Subdirector').values('id').first()                        
                # Obtener la instancia del jefe del departamento de Servicios Administrativos
                sub = trabajadores.objects.get(id=idsubdirectora['id'])
                solicitud.id_Subdirectora = sub
                solicitud.save()
                bitacora(request.user, 'Solicitud_Mantenimiento', 'Post', f'Folio: {solicitud.folio}', Departamento='dep_mantenimiento')
                return redirect('inicio')
        else:
            form = Peticionform()
            contexto = {'form': form, 'solicitud': solicitud, 'id': idSolicitud,'fecha':solicitud.fecha.strftime("%d/%m/%Y")}
        return render(request, 'dep_mantenimiento/layout/jMantenimiento/peticion.html', contexto)
   
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
        



# Función para obtener el historial de solicitudes para todos los usuarios de una solicitud especifica
def obtener_historial_solicitudes(request, solicitud_id):
    try:
        solicitud = Solicitud_Mantenimiento.objects.get(id=solicitud_id)
        historial = HistorialSolicitud.objects.filter(solicitud=solicitud_id)
        
        # Obtener el nombre completo del trabajador, jefe de departamento y subdirectora si existen
        nombre_trabajador = None
        nombre_jefe = None
        nombre_subdirectora = None
        nombre_Empleado= None
        nombre_Jefe_Mantenimiento = None
        if solicitud.id_Trabajador:
            nombre_trabajador = solicitud.id_Trabajador.nombre_completo()
        if solicitud.id_Jefe_Departamento:
            nombre_jefe = solicitud.id_Jefe_Departamento.nombre_completo()
        if solicitud.id_Subdirectora:
            nombre_subdirectora = solicitud.id_Subdirectora.nombre_completo()
        if solicitud.id_Empleado:
            nombre_Empleado = solicitud.id_Empleado.nombre_completo()
            
        if solicitud.id_Jefe_Mantenimiento:
            nombre_Jefe_Mantenimiento = solicitud.id_Jefe_Mantenimiento.nombre_completo()         
        
        solicitud_dict = {
            'id': solicitud.id,
            'id_Trabajador': solicitud.id_Trabajador_id,
            'nombre_trabajador': nombre_trabajador,
            'id_Jefe_Departamento': solicitud.id_Jefe_Departamento_id,
            'nombre_jefe': nombre_jefe,
            'id_Subdirectora': solicitud.id_Subdirectora_id,
            'nombre_subdirectora': nombre_subdirectora,
            'id_Empleado': solicitud.id_Empleado_id,
            'nombre_Empleado': nombre_Empleado,
            'id_Jefe_Mantenimiento': solicitud.id_Jefe_Mantenimiento_id,
            'nombre_Jefe_Mantenimiento': nombre_Jefe_Mantenimiento,
            'status': solicitud.status,
            'firma_Jefe_Departamento': solicitud.firma_Jefe_Departamento,
            'firma_Empleado': solicitud.firma_Empleado,
            'firma_Jefe_VoBo': solicitud.firma_Jefe_VoBo,
            'resolvio': solicitud.resolvio
        }
        
        historial_list = []
        for item in historial:
            historial_dict = {
                'nuevo_status': item.nuevo_status,
                'fecha': item.fecha.strftime('%d/%m/%Y'),
                'hora': item.hora.strftime('%H:%M'),
                'firma_Jefe_Departamento': item.firma_Jefe_Departamento,
                'firma_Empleado': item.firma_Empleado,
                'firma_Jefe_VoBo': item.firma_Jefe_VoBo,
                'resolvio': item.resolvio
            }
            historial_list.append(historial_dict)

        return JsonResponse({'historial': historial_list, 'solicitud': solicitud_dict})

    except Solicitud_Mantenimiento.DoesNotExist:
        return render(request, '404.html')













    
    

class Error404Views(TemplateView):
    template_name="404.html"



class Error403Views(TemplateView):
    template_name="403.html"



#@perssion  
@login_required
def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



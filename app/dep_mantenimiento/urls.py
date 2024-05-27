from django.urls import path
from . import views
from django.conf.urls import handler404,handler403
from .views import Empleado_required, JefeDep_required, JefeMan_required, Solicitante_required, Sub_required, generar_pdf, vistas_solicitantes,vistas_Jefe_Departamento,vistas_Empleados,vistas_Subdirectora,vistas_Jefe_Mantenimiento

urlpatterns = [
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    # Validar el inicio del usuario
    path('Ingresar', views.inicio, name='inicio'),

    # Enlaces del Docente
    path('CargarSolicitudes/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes.obtener_solicitudes), name='obtener_solicitudes'),
    path('Inicio/Docente/<int:id>/', Solicitante_required(views.vistas_solicitantes.cargar_Inicio), name='inicio_docente'),
    path('Docente/Ver_Solicitud/<int:solicitud_id>/',Solicitante_required(views.vistas_solicitantes.cargar_Solicitud), name='solicitud_detallada'),
    
    # Enlaces del para guardar el formulario
    path('Formulario/Docente/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes.cargar_Formulario), name='formulario_docente'),
    path('guardar/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes.guardar_datos_Docente), name='guardar_formulario_Docente'),
    #Enlaces del para Editar el formulario
    path('Formulario/Docente/Solicitud/<int:idSolicitud>/', Solicitante_required(views.vistas_solicitantes.cargar_Formulario_Editar), name='formulario_editar'),
   
    # Enlaces del jefe de Departamento
    path('CargarSolicitudesJdep/<int:id_Jefe>/',JefeDep_required( views.vistas_Jefe_Departamento.obtener_solicitudes), name='obtener_solicitudes_jefe_departamento'),
    path('Inicio/Jefe_Departamento/<int:id>/',JefeDep_required( views.vistas_Jefe_Departamento.cargar_Inicio), name='inicio_jefe_departamento'),
    path('Formulario/Jefe_Departamento/<int:id_JefeDepartamento>/',JefeDep_required( views.vistas_Jefe_Departamento.cargar_Formulario), name='formulario_jefe_departamento'),
    path('Formulario/Jefe_Departamento/Solicitud/<int:idSolicitud>/',JefeDep_required( views.vistas_Jefe_Departamento.editar_Formulario), name='editar_Formulario'),
    path('Firmar_Formulario/Jefe_Departamento/Solicitud/<int:idSolicitud>/',JefeDep_required( views.vistas_Jefe_Departamento.firmarFormulario), name='firmar_Formulario'),
    path('Firmar_Formulario_VoBo/Jefe_Departamento/Solicitud/<int:idSolicitud>/',JefeDep_required( views.vistas_Jefe_Departamento.firmarFormularioVoBo), name='firmar_Formulario_VoBo'),
    path('Jefe_Departamento/Ver_Solicitud/<int:solicitud_id>/',JefeDep_required(views.vistas_Jefe_Departamento.cargar_Solicitud), name='solicitud_Detallada'),

    # Enlaces del Empleados
    path('CargarSolicitudesEmpleados/<int:idEmpleado>/', Empleado_required(views.vistas_Empleados.obtener_solicitudes), name='obtener_solicitudes_empleados'),
    path('Inicio/Empleado/<int:id>/', Empleado_required(views.vistas_Empleados.cargar_Inicio), name='inicio_empleado'),
    path('Firmar_Formulario/Empleado/Solicitud/<int:idSolicitud>/',Empleado_required( views.vistas_Empleados.firmarFormulario), name='firmar_Formulario_Empleado'),
    path('Empleado/Ver_Solicitud/<int:solicitud_id>/',Empleado_required(views.vistas_Empleados.cargar_Solicitud), name='sol_detallada'),
   # Enlaces del Subdirectora
    path('CargarSolicitudesSubdirectora/<int:idSubdirectora>/', Sub_required(views.vistas_Subdirectora.obtener_solicitudes), name='obtener_solicitudes_subdirectora'),
    path('Inicio/Subdirectora/<int:id>/', Sub_required(views.vistas_Subdirectora.cargar_Inicio), name='inicio_subdirector_servicios'),
    path('Formulario/Subdirectora/<int:idSubdirectora>/',Sub_required( views.vistas_Subdirectora.cargar_Formulario), name='formulario_Subdirectora'),
    path('Formulario/Subdirectora/Solicitud/<int:idSolicitud>/',Sub_required( views.vistas_Subdirectora.editar_Formulario), name='editarformulario'),
    path('Formulario_Peticion/Subdirectora/Solicitud/<int:idSolicitud>/',Sub_required( views.vistas_Subdirectora.peticion_formulario), name='peticion_formulario'),
    path('Firmar_Formulario_VoBo/Subdirectora/Solicitud/<int:idSolicitud>/',Sub_required( views.vistas_Subdirectora.firmarFormularioVoBo), name='firmarFormulario_VoBo'),
    path('Subdirectora/Ver_Solicitud/<int:solicitud_id>/',Sub_required(views.vistas_Subdirectora.cargar_Solicitud), name='solicitudDET'),
    path('Subdirectora/Historico_Empleados/',Sub_required(views.vistas_Subdirectora.cargarHistorico), name='cargarHistorico'),

   # Enlaces del Jefe de Mantenimiento
    path('CargarSolicitudesJefeMantenimiento/<int:idJefeMantenimiento>/', JefeMan_required(views.vistas_Jefe_Mantenimiento.obtener_solicitudes), name='obtener_solicitudes_jefe_mantenimiento'),
    path('Inicio/Jefe_Mantenimiento/<int:id>/', JefeMan_required(views.vistas_Jefe_Mantenimiento.cargar_Inicio), name='inicio_jefe_mantenimiento'),
    path('Formulario_Rechazar/Jefe_Mantenimiento/Solicitud/<int:idSolicitud>/',JefeMan_required( views.vistas_Jefe_Mantenimiento.rechazarFormulario), name='rechazarFormulario'),
     path('Formulario_Peticion/Jefe_Mantenimiento/Solicitud/<int:idSolicitud>/',JefeMan_required( views.vistas_Jefe_Mantenimiento.peticionFormulario), name='peticionFormulario'),
  
    path('Jefe_Mantenimiento/Ver_Solicitud/<int:solicitud_id>/',JefeMan_required(views.vistas_Jefe_Mantenimiento.cargar_Solicitud), name='solicitudDetallada'),
    # Eliminar solicitud
     path('eliminar-solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
     
   #Detalle solicitud
    path('CargarSolicitudDetallada/<int:solicitud_id>/', views.obtener_historial_solicitudes, name='cargar_historial_solicitudes'),
   #generar PDF 

   path('generar-pdf/<int:solicitud_id>/', generar_pdf, name='generar_pdf'),
   
]

handler404 = views.Error404Views.as_view()
handler403 = views.Error403Views.as_view()
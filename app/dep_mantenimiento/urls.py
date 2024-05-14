from django.urls import path
from . import views
from django.conf.urls import handler404,handler403
from .views import Empleado_required, JefeDep_required, JefeMan_required, Solicitante_required, Sub_required, vistas_solicitantes_cargar_inicio,vistas_Jefe_Departamento_cargar_inicio,vistas_Empleados,vistas_Subdirectora,vistas_Jefe_Mantenimiento

urlpatterns = [
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    # Validar el inicio del usuario
    path('Ingresar', views.inicio, name='inicio'),

    # Enlaces del Docente
    path('CargarSolicitudes/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.obtener_solicitudes), name='obtener_solicitudes'),
    path('Inicio/Docente/<int:id>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.cargar_Inicio), name='inicio_docente'),
    # Enlaces del para guardar el formulario
    path('Formulario/Docente/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.cargar_Formulario), name='formulario_docente'),
    path('guardar/<int:id_Docente>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.guardar_datos_Docente), name='guardar_formulario_Docente'),
    #Enlaces del para Editar el formulario
    path('Formulario/Docente/Solicitud/<int:idFormulario>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.cargar_Formulario_Editar), name='formulario_editar'),
    path('editar/<int:idFormulario>/', Solicitante_required(views.vistas_solicitantes_cargar_inicio.edtiarFormulario), name='edtiarFormulario'),
    # Enlaces del jefe de Departamento
    path('CargarSolicitudesJdep/<int:id_Jefe>/',JefeDep_required( views.vistas_Jefe_Departamento_cargar_inicio.obtener_solicitudes), name='obtener_solicitudes_jefe_departamento'),
    path('Inicio/Jefe_Departamento/<int:id>/',JefeDep_required( views.vistas_Jefe_Departamento_cargar_inicio.cargar_Inicio), name='inicio_jefe_departamento'),
    path('Formulario/Jefe_Departamento/<int:id_JefeDepartamento>/',JefeDep_required( views.vistas_Jefe_Departamento_cargar_inicio.cargar_Formulario), name='formulario_jefe_departamento'),
    path('Formulario/Jefe_Departamento/Solicitud/<int:idSolocitud>/',JefeDep_required( views.vistas_Jefe_Departamento_cargar_inicio.editar_Formulario), name='editar_Formulario'),
    path('Firmar_Formulario/Jefe_Departamento/Solicitud/<int:idSolicitud>/',JefeDep_required( views.vistas_Jefe_Departamento_cargar_inicio.firmarFormulario), name='firmar_Formulario'),
   

    # Enlaces del Empleados
    path('CargarSolicitudesEmpleados/<int:idEmpleado>/', Empleado_required(views.vistas_Empleados.obtener_solicitudes), name='obtener_solicitudes_empleados'),
    path('Inicio/Empleado/<int:id>/', Empleado_required(views.vistas_Empleados.cargar_Inicio), name='inicio_empleado'),
   # Enlaces del Subdirectora
    path('CargarSolicitudesSubdirectora/<int:idSubdirectora>/', Sub_required(views.vistas_Subdirectora.obtener_solicitudes), name='obtener_solicitudes_subdirectora'),
    path('Inicio/Subdirectora/<int:id>/', Sub_required(views.vistas_Subdirectora.cargar_Inicio), name='inicio_subdirector_servicios'),
   # Enlaces del Jefe de Mantenimiento
    path('CargarSolicitudesJefeMantenimiento/<int:idJefeMantenimiento>/', JefeMan_required(views.vistas_Jefe_Mantenimiento.obtener_solicitudes), name='obtener_solicitudes_jefe_mantenimiento'),
    path('Inicio/Jefe_Mantenimiento/<int:id>/', JefeMan_required(views.vistas_Jefe_Mantenimiento.cargar_Inicio), name='inicio_jefe_mantenimiento'),
   
    
    # Eliminar solicitud
     path('eliminar-solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
   
]

handler404 = views.Error404Views.as_view()
handler403 = views.Error403Views.as_view()
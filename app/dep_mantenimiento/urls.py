from django.urls import path
from . import views
from django.conf.urls import handler404
#from .views import Views_Solicitantes, guardar_datos

urlpatterns = [
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    
    #Enlaces de empleado
    # path('empleado/inicio/', views.dashboard_empleado, name='Inicio_Empleado'),
    # path('empleado/firma_formulario/', views.dashboard_empleado_firma_form, name='Firma_form_Empleado'),
    # #Enlaces de solicitante
    # path('CargarSolicitudes/', views.Views_Solicitantes.obtener_solicitudes,name='CargarSolicitudes'),
   
    # path('solicitante/inicio/', views.Views_Solicitantes.cargar_Inicio,name='Inicio_Solicitante'),
    # #path('eliminar-solicitud/<int:id_solicitud>/', views.Views_Solicitantes.as_view(), name='eliminar_solicitud'),



    # path('guardar-datos/', guardar_datos, name='guardar_datos'),
    # #path('solicitante/inicio/', views.dashboard_solicitante, name='home.dep_mantenimiento'),
    # path('solicitante/formulario/', views.dashboard_solformulario, name='formulario_Solicitante'),
    # #Enlaces de subdirectora
    # path('subdirectora/inicio/', views.dashboard_subdirectora, name='Inicio_subdirectora'),
    # path('subdirectora/formulario/', views.dashboard_subd_formulario, name='Formulario_subdirectora'),
    # path('subdirectora/peticion_formulario/', views.dashboard_subdpeticion_form, name='Peticion_form_subdirectora'),
    # path('subdirectora/rechazar_formulario/', views.dashboard_subrechazar_form, name='Rechazar_form_subdirectora'),
    # #Enlaces de jefe del Departamento
    # path('jDep/inicio/', views.dashboard_jDep, name='Inicio_jDep'),
    # path('jDep/formulario/', views.dashboard_jDepformulario, name='Formulario_jDep'),
    # path('jDep/firma_formulario/', views.dashboard_jDepfirmar_form, name='Firma_form_jDep'),
    # #Enlaces de jefe de Mantenimiento
    # path('jMantenimiento/inicio/', views.dashboard_jMantenimeinto, name='Inicio_jMantenimiento'),
    # path('jMantenimiento/firmar_formulario/', views.dashboard_jMantenimeinto_firmar, name='Firma_form_jMantenimiento'),
    
    # path('jMantenimiento/estatus_formulario/', views.dashboard_jMantenimeinto_estatus, name='Estatus_jMantenimiento'),
    # path('jMantenimiento/estatus_formulario/rechazar_formulario/', views.dashboard_jMantenimeinto_rechazar, name='Rechazar_form_jMantenimiento'),
]

handler404 = views.Error404Views.as_view()
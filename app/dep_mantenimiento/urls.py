from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    #Enlaces de empleado
    #path('empleado/inicio /', views.dashboard_empleado, name='home.dep_mantenimiento'),
    #path('empleado/formulario/', views.dashboard_firma_form, name='firma_form.dep_mantenimiento'),
    #Enlaces de solicitante
    path('solicitante/inicio/', views.dashboard_solicitante, name='home.dep_mantenimiento'),
    path('solicitante/formulario/', views.dashboard_solformulario, name='formulario.dep_mantenimiento'),
    #Enlaces de subdirectora
    #path('subdirectora/inicio/', views.dashboard_subdirectora, name='home.dep_mantenimiento'),
    #path('subdirectora/formulario/', views.dashboard_subd_formulario, name='formulario.dep_mantenimiento'),
    #path('subdirectora/peticion_formulario/', views.dashboard_subdpeticion_form, name='peticion_form.dep_mantenimiento'),
    #path('subdirectora/rechazar_formulario/', views.dashboard_subrechazar_form, name='rechazar_form.dep_mantenimiento'),
    #Enlaces de jefe del Departamento
    #path('jDep/inicio/', views.dashboard_jDep, name='home.dep_mantenimiento'),
    #path('jDep/formulario/', views.dashboard_jDepformulario, name='formulario.dep_mantenimiento'),
    #path('jDep/firma_formulario/', views.dashboard_jDepfirmar_form, name='firma_form.dep_mantenimiento'),
    #Enlaces de jefe de Mantenimiento
    #path('jMantenimiento/inicio/', views.dashboard_jMantenimeinto, name='home.dep_mantenimiento'),
    #path('jMantenimiento/firmar_formulario/', views.dashboard_jMantenimeinto_firmar, name='firma_form_VoBo.dep_mantenimiento'),
    
    #path('jMantenimiento/estatus_formulario/', views.dashboard_jMantenimeinto_estatus, name='estatus.dep_mantenimiento'),
    #path('jMantenimiento/estatus_formulario/rechazar_formulario/', views.dashboard_jMantenimeinto_rechazar, name='rechazar_form.dep_mantenimiento'),
]

handler404 = views.Error404Views.as_view()
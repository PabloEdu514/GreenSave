from django.urls import path
from . import views
from django.conf.urls import handler404


urlpatterns = [
    path('', views.dashboard, name='home.Empleados'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

]

handler404 = views.Error404Views.as_view()
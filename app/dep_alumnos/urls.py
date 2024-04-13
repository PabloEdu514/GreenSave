from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.home, name="home.dep_alumnos"),
]


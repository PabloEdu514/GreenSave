from django.contrib import admin
from django.urls import include, path
from main.views import *
import mfa
import mfa.TrustedDevice

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('devices/add/', mfa.TrustedDevice.add,name="mfa_add_new_trusted_device"), # This short link to add new trusted device
    path('registered/',registered,name='registered')
     #login
    #path('accounts/', include('django.contrib.auth.urls')),

]
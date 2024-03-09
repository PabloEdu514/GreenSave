from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from mfa.helpers import has_mfa




#Comentado para hacer el login
def login_view(request):
    msg = {}
    form = AuthenticationForm()
    form.fields['username'].widget.attrs.update({'class': 'form-control','aria-describedby':'basic-addon1'})
    form.fields['password'].widget.attrs.update({'class': 'form-control','aria-describedby':'basic-addon2'})
    if request.method == "POST":
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            menerror = "Credenciales no válidas"
            context = {
                'form': form,
                'msg': menerror,
            }
            return render(request, 'main/accounts/login.html', context)
        password = request.POST['password']
        user = auth.authenticate(username=user.username, password=password)
        form = AuthenticationForm(None, request.POST)
        form.fields['username'].widget.attrs.update({'class': 'form-control','aria-describedby':'basic-addon1'})
        form.fields['password'].widget.attrs.update({'class': 'form-control','aria-describedby':'basic-addon2'})
        if user is not None and user.is_active:
            res =  has_mfa(username = user.username,request=request) # has_mfa returns false or HttpResponseRedirect
            if res:
                return res
            return create_session(request,username=user.username) 
            #log_user_in is a function that handles creatung user session, it should be in the setting file as MFA_CALLBACK
            #auth.login(request, user)
            #request.session.set_expiry(0)
            #return redirect('home')
        else:
            msg = 'Credenciales no válidas'
            
    context = {
        'form': form,
        'msg': msg,
        'invalid':True,
    }
    return render(request, 'main/accounts/login.html', context)

def create_session(request,username):
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    login(request, user)
    res =  has_mfa(username = user.username,request=request) # has_mfa returns false or HttpResponseRedirect
    if res==False:
        return HttpResponseRedirect(reverse('start_new_otop'))
    #request.session.set_expiry(100)
    return HttpResponseRedirect(reverse('home'))

@login_required()
def registered(request):
    return render(request,"main/layout/home.html",{"registered":True})

@login_required(login_url='/login/')
def logout_view(request):
    try:
        logout(request)
    except KeyError:
        pass
    return redirect('home')

    
@login_required(login_url='/login/')
def home(request):
    username = request.user
    user=User.objects.get(username=username)
    user.backend='django.contrib.auth.backends.ModelBackend'
    res =  has_mfa(username = user.username,request=request) # has_mfa returns false or HttpResponseRedirect
    if res==False:
        return HttpResponseRedirect(reverse('start_new_otop'))
    return render(request,'main/layout/home.html',{})

"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from django.conf.global_settings import PASSWORD_HASHERS as DEFAULT_PASSWORD_HASHERS


#CONFIGURACIÓN DE SEGURIDAD *** MUCHA ATENCIÓN ***
#ESTABLECER UNA VEZ QUE EL SERVIDOR SE HA COLOCADO CON CERTIFICADO SSL

#CONFIGURACIÓN HTTPS
#SECURE_HSTS_SECONDS = 3600
#CAMBIAR VALOR A 31536000, DESPUÉS DE LA ETAPA DE PRUEBAS

#HABILITAR SÓLO CONEXIONES SSL(HTTPS)
#SECURE_SSL_REDIRECT=True

#PROTECCIÓN DE COOKIES CONTRA ATAQUES DE HIJACKING
#SESSION_COOKIE_SECURE=True

#Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
#CSRF_COOKIE_SECURE=True

#Without this, your site is potentially vulnerable to attack via an insecure connection to a subdomain. Only set this to True if you are certain that all subdomains of your domain should be served exclusively via SSL.
#SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True
# CAMBIAR A FALSE DESPUÉS DE LAS PRUEBAS

#SECURE_HSTS_PRELOAD=True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x&7$)!$nj9#ca(3s%xln!m_^18_$+=5nt$z8s^chlntq570m6u'



ALLOWED_HOSTS = ['rh.morelia.tecnm.mx','64.225.125.20','127.0.0.1', 'localhost','*']


# Application definition

INSTALLED_APPS = [
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'main',
    'dep',
    'dep_alumnos',
    'mfa',
    'sslserver',
    'crispy_forms',
   
    'dep_mantenimiento',
    'django.contrib.admin',#Admin hasta abajo porque si no estorba para el logout
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'mysite.urls'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap4"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend",]

# vida de sesión 8 hrs
SESSION_COOKIE_AGE=28800

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASE_ROUTERS = ['mysite.dbRouter.DepRouter', 'mysite.dbRouter.AuthRouter','mysite.dbRouter.SARHRouter','mysite.dbRouter.MSRouter' ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'auth_db',
        'HOST': 'bases-datos',
        'PORT': '5432',
        'USER': 'adminsarh',
        'PASSWORD': 'adminsarhpassword.$',
    },
    'sarh_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dep_db',
        'USER': 'admindep',
        'PASSWORD': 'admindeppassword.$',
        'HOST': 'bases-datos',
        'PORT': '5432',
    },
         'dep_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dep_db',
        'USER': 'admindep',
        'PASSWORD': 'admindeppassword.$',
        'HOST': 'bases-datos',
        'PORT': '5432',
    },
         #Base de Datos de mantenimiento y el usuario que se encarga es admindep
        'ms_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ms_db',
        'USER': 'admindep',
        'PASSWORD': 'admindeppassword.$',
        'HOST': 'bases-datos',
        'PORT': '5432',
    }
         
         
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    #  {
    #      'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #      'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    #  },
    #  {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    #  },
    #  {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'es-MX'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# Email Configurations

# DEFAULT_FROM_EMAIL = ''
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER = 'nocontrol@morelia.tecnm.mx'
EMAIL_HOST_PASSWORD = 'su_contrasenna'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'media/'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/login/'
LOGOUT_REDIRECT_URL = 'home'

# Assets Management
#ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/softui') 

MFA_UNALLOWED_METHODS=('U2F','FIDO2','Email','Trusted_Devices')   # Methods that shouldn't be allowed for the user
MFA_LOGIN_CALLBACK="main.views.create_session"      # A function that should be called by username to login the user in session
MFA_RECHECK=True           # Allow random rechecking of the user
MFA_RECHECK_MIN=10         # Minimum interval in seconds
MFA_RECHECK_MAX=30         # Maximum in seconds
MFA_QUICKLOGIN=True        # Allow quick login for returning users by provide only their 2FA
MFA_HIDE_DISABLE=('',)     # Can the user disable his key (Added in 1.2.0).
MFA_REDIRECT_AFTER_REGISTRATION="registered"
MFA_SUCCESS_REGISTRATION_MSG="Seguir en SIGA"
MFA_ALWAYS_GO_TO_LAST_METHOD=True
MFA_ENFORCE_RECOVERY_METHOD=False
MFA_RENAME_METHODS={"TOTP":"Aplicación de Autenticación"}
PASSWORD_HASHERS=DEFAULT_PASSWORD_HASHERS #Comment if PASSWORD_HASHER already set
PASSWORD_HASHERS += ['mfa.recovery.Hash']
RECOVERY_ITERATION = 1 #Number of iteration for recovery code, higher is more secure, but uses more resources for generation and check...
TOKEN_ISSUER_NAME="SIGAapp"      #TOTP Issuer name

U2F_APPID="https://localhost:9001"    #URL For U2F
FIDO_SERVER_ID="localhost"      # Server rp id for FIDO2, it the full domain of your project
FIDO_SERVER_NAME="SIGAapp"

DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
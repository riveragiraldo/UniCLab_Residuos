"""
Django settings for inventarioreac project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os

from pathlib import Path

# Para DB en render
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h3d7k6@k)1sk)y961&1yk=kjax7un8quf2480&z&ler$o!=e!l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reactivos',
    'captcha',
    'import_export',
    "django_apscheduler",
    'crispy_forms',
    'dir_lab',
    'residuos', 
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

ROOT_URLCONF = 'inventarioreac.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'inventarioreac.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
       	'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Reactivos',
        'USER': 'postgres',
        'PASSWORD': 'Comput2011*',
        'HOST': 'localhost',
        'PORT': '5432',
        }
}

DATABASES['default'] = dj_database_url.config(
    default='postgres://dirlabor_man_unal:PpKGklM6fx9Vxq0y0xAcEmJZjuLt8BPj@dpg-coa15e0cmk4c73e7uo30-a.oregon-postgres.render.com/dejango_reactivos'
)



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es-419'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

#Ubicacioón de archivos adjuntos

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
BASE_URL = 'https://laboratorios.manizales.unal.edu.co/UniCLab'

# Tiempo de inactividad en segundos antes de que la sesión expire (60 minutos)
SESSION_COOKIE_AGE = 28800  # 8 horas




# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

AUTH_USER_MODEL = 'reactivos.User'

# RECAPTCHA_PUBLIC_KEY = '6LeGjm4nAAAAABXTrZCNgjlT3P57fyB5oQI0NdpB'
# RECAPTCHA_PRIVATE_KEY = '6LeGjm4nAAAAABdT4YwpvZ_xZ1cwQ07xFJDjSgrI'

# # Opciones disponibles: 'image', 'audio', 'checkbox'
# RECAPTCHA_TYPE = 'image'  # Puedes elegir el tipo que prefieras

# Configuración para utilizar el backend de correo electrónico SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Configuración para el servidor de correo SMTP
EMAIL_HOST = 'smtp.gmail.com'  # Dirección del servidor SMTP
EMAIL_PORT = 587  # Puerto para la conexión (generalmente 587 para TLS o 465 para SSL)
EMAIL_USE_TLS = True  # Configura como True si se requiere TLS (usar EMAIL_USE_SSL en caso de SSL)
EMAIL_HOST_USER = 'uniclab_man@unal.edu.co'  # Usuario para autenticación SMTP
EMAIL_HOST_PASSWORD = 'ayff mfdx yebl vnko'  # Contraseña para autenticación SMTP

# Correo del remitente predeterminado
DEFAULT_FROM_EMAIL = 'Notificaciones Dirección de Laboratorios <uniclab_man@unal.edu.co>'

LOGIN_REDIRECT_URL = "/UniCLab/"
# LOGIN_URL = "accounts/login/?next=/"
LOGIN_URL = "/UniCLab/accounts/login/"


CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_TIMEOUT = 20
CAPTCHA_LETTER_ROTATION=(-30,30)
CAPTCHA_FONT_SIZE=35
CAPTCHA_BACKGROUND_COLOR='transparent'

CRISPY_TEMPLATE_PACK = 'bootstrap4'






from pathlib import Path
import os       
import environ       
import dj_database_url 

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# Leer .env si existe (local)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env("SECRET_KEY", default='django-insecure-clave-temporal-local')

# IMPORTANTE: DEBUG lee del entorno. En Render será False.
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["*"] 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # LIBRERIAS DE TERCEROS
    'rest_framework', 
    'drf_yasg',

    # ===============Propias==================
    'cuentas',
    'alumnos',
    'tareas',
    'galeria',
    'informes',
    'contacto',
    'shop',
    'api_libros',
    'scraper',
    'estadisticas',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <--- CRÍTICO
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'segundoParcial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'segundoParcial.wsgi.application'

# Base de datos Híbrida (SQLite Local / Postgres Render)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

LANGUAGE_CODE = 'es-ar' 
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (CORREGIDO) ---
STATIC_URL = 'static/'

# 1. Dónde están tus estilos ahora (styles.css)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 2. Dónde se guardarán al subir a Render
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 3. Motor de almacenamiento
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGOUT_REDIRECT_URL = '/'

# --------------------------------------------------------
# CONFIGURACIÓN DE EMAIL PROFESIONAL (BREVO)
# --------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Tu usuario de login en Brevo (tu correo)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# La clave larga que acabas de generar en el panel SMTP
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# IMPORTANTE: Brevo exige que el remitente sea un email validado
# Por defecto usa tu propio email de registro
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER')
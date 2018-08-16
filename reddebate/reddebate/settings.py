# coding=utf-8
"""
Django settings for reddebate project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from os.path import join


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vlf=awhlkhl@b1q7bo92mj^-@dh0fv0zx5mz%qsitx7zfc3s62'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'http://reddebate.cl/',
    'http://146.83.216.233/'
]

TEMPLATE_DIRS=(
    join(BASE_DIR, 'templates'),
    )
# Application definition

INSTALLED_APPS = [
    'resumen',
    'debate', #aplicación de "Ver debate"
    'perfil',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'social_django',
    'channels',
    'reddebate',
    'taggit',
]
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
        },
        'ROUTING': 'reddebate.routing.channel_routing',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'reddebate.urls'

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
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'django.template.context_processors.media',

            ],
        },
    },
]

WSGI_APPLICATION = 'reddebate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reddebate',
        'USER': 'redusuario',
        'PASSWORD': 'redpass',
        'HOST': '127.0.0.1',
        #'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

APPEND_SLASH=False

#AUTHENTICATION_BACKENDS = (
    # Facebook 'social.backends.facebook.FacebookOAuth2',
    # Twitter 'social.backends.twitter.TwitterOAuth',
    # Django 'django.contrib.auth.backends.ModelBackend', )
    # Facebook Keys SOCIAL_AUTH_FACEBOOK_KEY = 'q23456uhgf'
    #SOCIAL_AUTH_FACEBOOK_SECRET = 'qw4trgfdxc'
    # Twitter Keys SOCIAL_AUTH_TWITTER_KEY = '123456yhgfdsvc'
    #SOCIAL_AUTH_TWITTER_SECRET = '123456789okjhgfd'


AUTHENTICATION_BACKENDS = (
 #'social.backends.facebook.FacebookAppOAuth2',
 'social.backends.facebook.FacebookOAuth2',
 'social.backends.twitter.TwitterOAuth',
 'django.contrib.auth.backends.ModelBackend',
 )

#Facebook inicio de sesión con social-auth
SOCIAL_AUTH_FACEBOOK_KEY = '671191633038377'
SOCIAL_AUTH_FACEBOOK_SECRET = '1a94e2cf456e1c20b98a1ac8a2cb50f7'

#Twitter inicio de sesión con social-auth
SOCIAL_AUTH_TWITTER_KEY = 'XTnczMpQ7tq6uQcQEGFNUl3jR'
SOCIAL_AUTH_TWITTER_SECRET = 'HsiSFdrB3IB7e1IPr1Hs4LTxRpB2Tbd61I97YTEDAUNjLovSjt'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

#luego de la autentificacion del usuario redirecciona a la URL, entonces solo será necesario el decorador @login_required.
SOCIAL_AUTH_LOGIN_REDIRECT_URL =  '/resumen/'
LOGIN_URL = '/'
LOGOUT_REDIRECT_URL = '/resumen/'
SOCIAL_AUTH_FACEBOOK_SCOPE =['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
    }
#SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
#SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'


#SOCIAL_AUTH_USER_MODEL = 'auth.User'

#SOCIAL_AUTH_PIPELINE = (
#Obtiene las instancias de social_user y user
#'social.pipeline.social_auth.social_details',
#'social.pipeline.social_auth.social_uid',
#'social.pipeline.social_auth.auth_allowed',
#Recibe según el user.email la instancia del usuario y lo reemplaza con uno que recibió anteriormente
#'social.pipeline.social_auth.social_user',
#'social.pipeline.social_auth.associate_by_email',
#Intenta crear un username válido
#'social.pipeline.user.get_username',
#Crea un nuevo usuario si todavía no existe
#'social.pipeline.user.create_user',
#Trata de asociar las cuentas
#'social.pipeline.social_auth.associate_user',
#Recibe y actualiza social_user.extra_data
#'social.pipeline.social_auth.load_extra_data',
#Actualiza los campos de la instancia user con la información que obtiene vía backend
#'social.pipeline.user.user_details',
#Función creado por mi que termina de realizar la autenticación
#'apps.reddebate.pipelines.login',
#)


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS= ( os.path.join(BASE_DIR,'static'),
    )

MEDIA_URL = '/media/'
MEDIA_ROOT = ( os.path.join(BASE_DIR,'media')
    )

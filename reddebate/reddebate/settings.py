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

ALLOWED_HOSTS = ['*']

TEMPLATE_DIRS=(
    join(BASE_DIR, 'templates'),
    )
# Application definition

INSTALLED_APPS = [
    'resumen',
    'debate', #aplicación de "Ver debate"
    'perfil',
    'moderacion',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'channels',
    'reddebate',
    'taggit',
    'django_extensions',
]

# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

LOGIN_REDIRECT_URL = '/'

SITE_ID = 1

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
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'reddebate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates', 'allauth')],
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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'resumen.context_processors.listado_notificacion',
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

AUTHENTICATION_BACKENDS = (
 'django.contrib.auth.backends.ModelBackend',
 'social_core.backends.github.GithubOAuth2',
 'social_core.backends.twitter.TwitterOAuth',
 'social_core.backends.facebook.FacebookOAuth2',
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
 )

LOGIN_URL = 'home'
LOGOUT_URL = 'home'
LOGIN_REDIRECT_URL = 'index'

 # Facebook Keys
SOCIAL_AUTH_FACEBOOK_KEY = '309804006235802'
SOCIAL_AUTH_FACEBOOK_SECRET = '99e58f77068352b2814e8dc7313a3a42'
 # Twitter Keys
SOCIAL_AUTH_TWITTER_KEY = 'nJ962jcMQu7TZsUSkQMuw2eJQ'
SOCIAL_AUTH_TWITTER_SECRET = 'nna8b4j1exRNQTKH2XaX1TCHI7UQXdaECajws6gXLRqpUBNzhD'

SOCIAL_AUTH_GITHUB_KEY = '7f30c97d73bb43ceb0eb'
SOCIAL_AUTH_GITHUB_SECRET = '2e0beb0062ddbe1520126cecc0e9316d186bc346'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='731660534155-f03jnm6o1fa7abisiujult4t85qq2316.apps.googleusercontent.com'  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'bSVqtrLWEmvYHIRDn82VN1lb' #Paste Secret Key
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

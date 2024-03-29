"""
Django settings for restful01 project.

Generated by 'django-admin startproject' using Django 2.1.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+$n6ak4365@^q+b*p(bkao@%rnwp37woz(@10_xc8=a4@8(b(p'

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
    # Django REST framework
    'rest_framework',
    # Toys application
    'toys.apps.ToysConfig',
    # Drone application
    'drones.apps.DronesConfig',
    # Django filters
    'django_filters',
    # adding token based authentication
    'rest_framework.authtoken',
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

ROOT_URLCONF = 'restful01.urls'

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

WSGI_APPLICATION = 'restful01.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drones',
        # Replace username with your desired user name
        'USER': 'emilextrig',
        # Replace password with your desired password
        'PASSWORD': 'postgres',
        # Replace 127.0.0.1 with the PostgreSQL host
        'HOST': '127.0.0.1',
        # Replace 5432 with the PostgreSQL configured port
        # in case you aren't using the default port
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    # setting for pagination.
    'DEFAULT_PAGINATION_CLASS': 'drones.custompagination.LimitOffsetPaginationWithUpperBound',
    'PAGE_SIZE': 5,
    # settings for backend filter.
    'DEFAULT_FILTER_BACKENDS':(
        'django_filters.rest_framework.DjangoFilterBackend', # for field filtering. specify fields we want to filter against.
        'rest_framework.filters.OrderingFilter', # clients controls how results are ordered  with single query param.
        'rest_framework.filters.SearchFilter',), # clients makes request to search on multiple fields with a single query
    # adding authentication to our restapi
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES' : (
        'rest_framework.throttling.AnonRateThrottle',  # Throttling for anonymous use
        'rest_framework.throttling.UserRateThrottle',  #  Throttling for user both auth. and non auth.
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '300/hour',  # 4 request per hour for anonymous users.
        'user': '500/hour',  # 50 request per hour for user endpoint 
        'drones': '600/hour',   # 100 request per hour for drones endpoint 
        'pilots': '550/hour',   # 60 request per hour for pilots endpoint 
    },
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}


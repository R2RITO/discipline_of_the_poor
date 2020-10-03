"""
Django settings for discipline_of_the_poor project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.utils.translation import gettext_lazy as _
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=w3lpt9824d8yc))jj&mb7j)jfyfa0_7_j@4emf*w@!pxgtiel'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

# Media handling

MEDIA_ROOT = os.environ.get('BASE_MEDIA_ROOT')
MEDIA_URL = os.environ.get('MEDIA_URL')
BUDGET_MEDIA_FOLDER = os.environ.get('BUDGET_MEDIA_FOLDER')

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'budget',
    'dotp_users',
    'guardian',
    'reversion',
    'drf_yasg',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'budget.middlewares.db_middleware.RoutingMiddleware',
    'budget.middlewares.audit_middleware.CustomAuditMiddleware',
]

ROOT_URLCONF = 'discipline_of_the_poor.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

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

WSGI_APPLICATION = 'discipline_of_the_poor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DEFAULT_DATABASE_NAME'),
        'USER': os.environ.get('DEFAULT_DATABASE_USER'),
        'PASSWORD': os.environ.get('DEFAULT_DATABASE_PASSWORD'),
        'HOST': os.environ.get('DEFAULT_DATABASE_HOST'),
        'PORT': os.environ.get('DEFAULT_DATABASE_PORT'),
    },
    'regular': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('REGULAR_DATABASE_NAME'),
        'USER': os.environ.get('REGULAR_DATABASE_USER'),
        'PASSWORD': os.environ.get('REGULAR_DATABASE_PASSWORD'),
        'HOST': os.environ.get('REGULAR_DATABASE_HOST'),
        'PORT': os.environ.get('REGULAR_DATABASE_PORT'),
    },
    'premium': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PREMIUM_DATABASE_NAME'),
        'USER': os.environ.get('PREMIUM_DATABASE_USER'),
        'PASSWORD': os.environ.get('PREMIUM_DATABASE_PASSWORD'),
        'HOST': os.environ.get('PREMIUM_DATABASE_HOST'),
        'PORT': os.environ.get('PREMIUM_DATABASE_PORT'),
    },
}

DATABASE_ROUTERS = [
    'budget.middlewares.db_middleware.CustomDatabaseRouter'
]


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'dotp_users.DotpUser'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=150),
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'discipline_of_the_poor.permissions.CustomObjectPermissions'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework_guardian.filters.ObjectPermissionsFilter',
    ],
}

GUARDIAN_RAISE_403 = True
ANONYMOUS_USER_NAME = None
GUARDIAN_MONKEY_PATCH = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]

# OpenApi swagger settings
SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'discipline_of_the_poor.urls.schema_info',
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_AUTO_SCHEMA_CLASS': 'drf_yasg_examples.SwaggerAutoSchema',
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Celery settings

CELERY_BROKER = os.environ.get('CELERY_BROKER')

# Mail settings

DOTP_EMAIL = os.environ.get('DOTP_EMAIL')

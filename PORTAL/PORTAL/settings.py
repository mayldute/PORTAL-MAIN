"""
Django settings for PORTAL project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from config import DB_LOGIN, DB_PASS, DB_HOST, DB_PORT, DB_NAME, DJ_SCRT_KEY, FROM_DEFAULT_EMAIL, FROM_EMAIL_PASSWORD, FROM_EMAIL_USER
from django.utils.log import RequireDebugFalse, RequireDebugTrue

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = 'http://127.0.0.1:8000'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJ_SCRT_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_filters',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.yandex',
       
    'posts',
    'profilepage.apps.ProfilepageConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'PORTAL.urls'

TEMPLATES = [
   {
       'BACKEND': 'django.template.backends.django.DjangoTemplates',
       'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'PORTAL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_LOGIN,
        'PASSWORD': DB_PASS,
        'HOST': DB_HOST, 
        'PORT': DB_PORT, 
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', 
    'allauth.account.auth_backends.AuthenticationBackend', 
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), 
    }
}

ACCOUNT_EMAIL_REQUIRED = True 
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory" 
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True 

LOGIN_REDIRECT_URL = '/posts/'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEFAULT_FROM_EMAIL = FROM_DEFAULT_EMAIL

# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = FROM_EMAIL_USER
# EMAIL_HOST_PASSWORD = FROM_EMAIL_PASSWORD
# EMAIL_USE_SSL = True

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'console_debug': {
#             'format': '{asctime} {levelname} {message}',
#             'style': '{',
#         },
#         'console_warning': {
#             'format': '{asctime} {levelname} {pathname} {message}',
#             'style': '{',
#         },
#         'file_general': {
#             'format': '{asctime} {levelname} {module} {message}',
#             'style': '{',
#         },
#         'file_errors': {
#             'format': '{asctime} {levelname} {message} {pathname}',
#             'style': '{',
#         },
#         'security': {
#             'format': '{asctime} {levelname} {module} {message}',
#             'style': '{',
#         },
#         'mail_errors': {
#             'format': '{asctime} {levelname} {message} {pathname}',
#             'style': '{',
#         },
#     },
#     'filters': {
#         'require_debug_true': {
#             '()': RequireDebugTrue,
#         },
#         'require_debug_false': {
#             '()': RequireDebugFalse,
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'filters': ['require_debug_true'], 
#             'formatter': 'console_debug',
#         },
#         'console_warning': {
#             'level': 'WARNING',
#             'class': 'logging.StreamHandler',
#             'filters': ['require_debug_true'],  
#             'formatter': 'console_warning',
#         },
#         'file_general': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filters': ['require_debug_false'], 
#             'filename': os.path.join('logs', 'general.log'),
#             'formatter': 'file_general',
#         },
#         'file_errors': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join('logs', 'errors.log'),
#             'formatter': 'file_errors',
#         },
#         'file_security': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join('logs', 'security.log'),
#             'formatter': 'security',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'], 
#             'formatter': 'mail_errors',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'console_warning', 'file_general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file_errors', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['file_errors', 'mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['file_errors'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.db.backends': {
#             'handlers': ['file_errors'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'django.security': {
#             'handlers': ['file_security'],
#             'level': 'INFO',
#             'propagate': False,
#         },
#     },
# }
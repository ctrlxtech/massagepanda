"""
Django settings for mpproject project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import os.path
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('/etc/keys.json') as f:
    keys = json.load(f)
if keys is not None:
    for (n, v) in keys.items():
        exec('%s=%s' % (n, repr(v)))

SF_ZIPCODES = {94101, 94102, 94103, 94104, 94105, 94107, 94108, 94109, 94110, 94111, 94112, 94114, 94115, 94116, 94117, 94118, 94119, 94120, 94121, 94122, 94123, 94124, 94125, 94126, 94127, 94128, 94129, 94130, 94131, 94132, 94133, 94134, 94137, 94139, 94140, 94141, 94142, 94143, 94144, 94145, 94146, 94147, 94151, 94153, 94154, 94156, 94158, 94159, 94160, 94161, 94162, 94163, 94164, 94171, 94172, 94177, 94188, 94199}
TAX = 0.0

REFER_BONUS = 20.0

ALLOWED_HOSTS = [
'*'
]

SITE_ID = 1

ADMINS = (('Kevin Chen', 'yuechen1989@gmail.com'))
MANAGERS = (('Kevin Chen', 'yuechen1989@gmail.com'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False
}

# Application definition

INSTALLED_APPS = (
    'nested_inline',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'index',
    'services',
    'payment',
    'manager',
    'customers',
    'referral',
    'feedback',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'mpproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'mpproject.context_processors.prod',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mpproject.wsgi.application'

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
elif 'MYSQL_CONFIG' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.environ['MYSQL_CONFIG'],
            }, 
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': '/etc/database.cnf',
            },
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_FROM_EMAIL = "support@massagepanda.com"

SERVER_EMAIL = "MassagePanda<do-not-reply@massagepanda.com>"

EMAIL_HOST = "smtp.mandrillapp.com"

EMAIL_HOST_USER = "support@massagepanda.com"

EMAIL_PORT = 587
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
MEDIA_ROOT = '/home/ubuntu/massagepanda/images/'
STATIC_ROOT = os.path.join(BASE_DIR, "..", "static")
STATIC_URL = '/static/'
LOGIN_URL = 'admin:login'

if os.path.isfile('/etc/debug'):
    MEDIA_URL = '/static/images/'
    DEBUG = True
else:
    # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
    # you run `collectstatic`).
    AWS_STORAGE_BUCKET_NAME = 'massagepanda-media-bucket'
    MEDIAFILES_LOCATION = 'media'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

ROLLBAR = {
    'access_token': '11d3ef845039461d93de971769845146',
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
}
import rollbar
rollbar.init(**ROLLBAR)

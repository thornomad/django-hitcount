"""
Django settings for example_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys
sys.path.insert(0, '../../django-hitcount')
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 't=d4ulc7kg99v4$d#s4ann+#&va0b2-npkq!qh19!l#_29@&$n'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth',
    'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles', 'blog', 'hitcount'
    )
MIDDLEWARE = ('django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware')
ROOT_URLCONF = 'example_project.urls'
WSGI_APPLICATION = 'example_project.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os
    .path.join(BASE_DIR, 'db.sqlite3')}}
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True, 'OPTIONS': {'debug': DEBUG, 'context_processors': [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages']}}]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'
HITCOUNT_KEEP_HIT_ACTIVE = {'minutes': 60}
HITCOUNT_HITS_PER_IP_LIMIT = 0
HITCOUNT_EXCLUDE_USER_GROUP = ()
HITCOUNT_KEEP_HIT_IN_DATABASE = {'seconds': 10}

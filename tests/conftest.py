# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                               'NAME': ':memory:'}},
        SITE_ID=1,
        SECRET_KEY='HitCounts Rock!',
        USE_I18N=True,
        USE_L10N=True,
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',

            'hitcount',
            'tests',
        ),
        ROOT_URLCONF = 'tests.urls',
        SESSION_ENGINE = 'django.contrib.sessions.backends.file',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            },
        ],
        # HitCount Variables (default values)
        HITCOUNT_KEEP_HIT_ACTIVE = {'days': 7},
        HITCOUNT_HITS_PER_IP_LIMIT = 0,
        HITCOUNT_EXCLUDE_USER_GROUP = (),
        HITCOUNT_KEEP_HIT_IN_DATABASE = {'days': 30},
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass

    # so we can reuse this function when testing directly from Django
    # via: ./runtests.py --django
    return settings

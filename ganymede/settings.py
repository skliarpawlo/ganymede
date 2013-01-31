import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
HEAP_PATH = os.path.join(BASE_PATH, "heap")
STATIC_ROOT = os.path.join(BASE_PATH, "static")

TEMPLATE_DIRS = (
    os.path.join( BASE_PATH, 'templates' ),
)

DATABASES = {
    'default': { # not used (sql alchemy instead)
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : '/tmp/sqlite_dump.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'testlib',
)

####################

SECRET_KEY = '=j%dl$72b*3aoqpqi)g)$rrfe-e+4$*k#f@8$=b#f@-u=v&amp;lgl'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'django.contrib.messages.middleware.MessageMiddleware',
     'ganymede.middle.GanymedeMiddleware',
    )

ROOT_URLCONF = 'ganymede.urls'

WSGI_APPLICATION = 'ganymede.wsgi.application'

ADMINS = (
    ('Pavlo Skliar', 'skliarpawlo@rambler.ru'),
    )

TIME_ZONE = 'Europe/Riga'

LANGUAGE_CODE = 'ua-uk'

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

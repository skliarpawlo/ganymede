import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# mars, vm
MODE = "mars"
USE_VSCREEN = True

BASE_URL = "ganymede.lun.ua"
SERVER_PORT = 80
if MODE == "vm" :
    BASE_URL = "vmdebian:8181"
    SERVER_PORT = 8181

BASE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
HEAP_PATH = os.path.join(BASE_PATH, "heap")
STATIC_ROOT = os.path.join(BASE_PATH, "static")

DATABASES = {
    'default': { # not used (sql alchemy instead)
        'ENGINE' : 'django.db.backends.sqlite3',
        'NAME' : '/tmp/sqlite_dump.db',
    }
}

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'testlib',
    'testing_runtime',
    'testing_runtime.web',
    'wtforms.ext.django',
)

####################

SECRET_KEY = '=j%dl$72b*3aoqpqi)g)$rrfe-e+4$*k#f@8$=b#f@-u=v&amp;lgl'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)
MIDDLEWARE_CLASSES = (
#    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'ganymede.middle.DbMiddleware',
    'ganymede.middle.UserAuthMiddleware',
    'ganymede.middle.ViewNameMiddleware',
)

ROOT_URLCONF = 'ganymede.urls'

WSGI_APPLICATION = 'ganymede.wsgi.application'

ADMINS = (
    ('Pavlo Skliar', 'skliarpawlo@rambler.ru'),
)

TIME_ZONE = 'Europe/Kiev'

LANGUAGE_CODE = 'en'

_ = lambda s: s
LANGUAGES = (
    ('uk', _('Ukrainian')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_HOST_USER = "lun.ua"
EMAIL_HOST_PASSWORD = "ytldb;bvjcnmyfkeyt"
EMAIL_FROM = "ganymede@lun.ua"
#EMAIL_USE_TLS = True

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

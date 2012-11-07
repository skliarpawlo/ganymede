# Django settings for ganymede project.
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "../"))
HEAP_PATH = os.path.join(BASE_PATH, "heap")

ADMINS = (
    ('Pavlo Skliar', 'skliarpawlo@rambler.ru'),
)

TIME_ZONE = 'Europe/Riga'

LANGUAGE_CODE = 'ua-uk'

SITE_ID = 1

USE_I18N = False

USE_L10N = False

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_PATH, "assets")
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_PATH, "ganymede", "static"),
    os.path.join(BASE_PATH, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=j%dl$72b*3aoqpqi)g)$rrfe-e+4$*k#f@8$=b#f@-u=v&amp;lgl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ganymede.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'ganymede.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join( BASE_PATH, 'templates' ),
)

INSTALLED_APPS = (
    #'django.contrib.auth',
    #'django.contrib.contenttypes',
    #'django.contrib.sessions',
    #'django.contrib.sites',
    #'django.contrib.messages',

    'django.contrib.staticfiles',
    'tests.seo_texts',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

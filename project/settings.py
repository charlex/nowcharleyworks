import os
from django.core.exceptions import SuspiciousOperation

ALLOWED_HOSTS = ['localhost', 'charley.pythonanywhere.com']

SECRET_KEY = "vl3n%)zav@@7w5*z*4i$h8r)@5xa$tr8=t$tgmbwll$%i*1jgg"

ADMINS = (
    ('Charley Bodkin', 'charley.bodkin@latimes.com'),
)
MANAGERS = ADMINS

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
    'compressor.filters.template.TemplateFilter'
]
COMPRESS_JS_FILTERS = [
    'compressor.filters.jsmin.JSMinFilter',
]

try:
    from settings_dev import *
except ImportError:
    from settings_prod import *

COMPRESS_ENABLED = True


# Settings paths that are handy to use other places
SETTINGS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.join(
    os.path.abspath(
        os.path.join(SETTINGS_DIR, os.path.pardir),
    ),
)
BASE_DIR = ROOT_DIR
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

TEMPLATE_DEBUG = DEBUG

# Gmail config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Localization
TIME_ZONE = 'America/Los_Angeles'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media and static files
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'templates', 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder'
)

# Templates
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(ROOT_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
)

# Web request stuff
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'project.urls'

# Installed apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'nowcharleyworks',
    'rockbot',
    'slackbot'
)

# Logging
MUNIN_ROOT = '/var/cache/munin/www/'

def skip_suspicious_operations(record):
  if record.exc_info:
    exc_value = record.exc_info[1]
    if isinstance(exc_value, SuspiciousOperation):
      return False
  return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
         },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(ROOT_DIR, 'django.log'),
            'maxBytes': 1024*1024*5, # 5MB,
            'backupCount': 0,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(module)s|%(process)d|%(thread)d|%(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s|%(message)s'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'logfile', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'p2p': {
            'handlers': ['console', 'logfile',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'toolbox': {
            'handlers': ['console', 'logfile',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'card_generator.views': {
            'handlers': ['console', 'logfile',],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'latprojects@gmail.com'
EMAIL_HOST_PASSWORD = 'ch@ndl3r'
EMAIL_USE_TLS = True

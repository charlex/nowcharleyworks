DEBUG = False
DEVELOPMENT, PRODUCTION = False, True
DEBUG_TOOLBAR = True
COMPRESS_ENABLED = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'charley$default',
        'USER': 'charley',
        'PASSWORD': 'ch@ndl3r',
        'HOST': 'charley.mysql.pythonanywhere-services.com',
    }
}
CACHES = {
    'default': {
        'LOCATION': 'my_cache_table',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
STATIC_URL = '/static/'
WSGI_APPLICATION = 'project.wsgi_prod.application'

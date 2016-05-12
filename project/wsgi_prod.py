import os
import sys

sys.path.append('/home/charley/code/nowcharleyworks/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

os.environ["CELERY_LOADER"] = "django"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import os, os.path, sys
sys.path.append('/opt/webapps/subscribe')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.stdout = sys.stderr
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

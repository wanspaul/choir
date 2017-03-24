import os
import socket
from django.core.wsgi import get_wsgi_application

if os.environ.get('DJANGO_SETTINGS_MODULE') is None:
    if socket.gethostname() == 'nsmsc.kr':
        print('production setting')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choir.settings.production')
    else:
        print('local setting')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choir.settings.local')

application = get_wsgi_application()


import os
import sys

path = os.path.realpath(os.path.join(__file__, os.path.pardir, 'src'))
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'f1web.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

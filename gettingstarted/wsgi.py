"""
WSGI config for gettingstarted project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
print("hello: I am from defualt module:1")
#from gettingstarted import settings

#print(SETTING)
# yey

# All `django.conf.settings` are also available
#print(DEBUG)
# True
import sys
from defaults import *

if sys.platform == 'linux2':
    DEBUG = TEMPLATE_DEBUG = False
elif sys.platform == 'win32':
    DEBUG = TEMPLATE_DEBUG = True

# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

# SESSION_ENGINE = "django.contrib.sessions.backends.cache"

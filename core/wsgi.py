"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = get_wsgi_application()

# WhiteNoise Settings
# application = WhiteNoise(application, root="/opt/services/djangoapp/src/staticfiles")
# application.add_files("/opt/services/djangoapp/src/staticfiles", prefix="more-files/")

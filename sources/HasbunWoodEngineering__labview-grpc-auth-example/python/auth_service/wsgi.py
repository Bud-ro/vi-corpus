import os

from django.core.wsgi import get_wsgi_application

# WSGI entrypoint for sync servers (e.g., gunicorn).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_service.settings")

# Expose the WSGI application callable.
application = get_wsgi_application()

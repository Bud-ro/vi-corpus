import os

from django.core.asgi import get_asgi_application

# ASGI entrypoint for async servers (e.g., uvicorn, daphne).
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auth_service.settings")

# Expose the ASGI application callable.
application = get_asgi_application()

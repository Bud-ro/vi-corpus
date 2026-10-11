from django.apps import AppConfig


class GrpcAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "grpc_auth"

    def ready(self) -> None:
        from . import signals  # noqa: F401

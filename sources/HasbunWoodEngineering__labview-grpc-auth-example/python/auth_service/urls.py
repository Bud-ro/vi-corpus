from django.contrib import admin
from django.urls import include, path

from grpc_auth import views as grpc_views
from django.http import Http404

# Loaded by Django because settings.py sets ROOT_URLCONF = "auth_service.urls".
urlpatterns = [
    # Django admin.
    path("admin/", admin.site.urls),
    # Custom password change UI (overrides allauth default view).
    path(
        "accounts/password/change/",
        grpc_views.password_change,
        name="account_change_password",
    ),
    # allauth account + MFA routes.
    path("accounts/", include("allauth.urls")),
    # Disable email management UI.
    path("accounts/email/", lambda request: (_ for _ in ()).throw(Http404())),
    # Simple post-login action hub.
    path("user-actions/", grpc_views.user_actions, name="user_actions"),
    # Client-initiated login completion page.
    path("app/complete/<uuid:session_id>/", grpc_views.login_complete),
]

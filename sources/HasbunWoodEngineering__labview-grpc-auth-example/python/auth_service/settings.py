from pathlib import Path
import os

# Project root directory.
BASE_DIR = Path(__file__).resolve().parent.parent

# Enable debug mode only when explicitly set to "1".
DEBUG = os.getenv("DJANGO_DEBUG") == "1"

# Secret key for cryptographic signing.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY not set")

# Comma-separated list of allowed Host headers.
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()
]
if not ALLOWED_HOSTS:
    raise RuntimeError("DJANGO_ALLOWED_HOSTS not set")

# Comma-separated list of trusted origins for CSRF protection.
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]

INSTALLED_APPS = [
    # Core Django apps
    "django.contrib.admin",  # Admin UI
    "django.contrib.auth",  # Users, groups, permissions
    "django.contrib.contenttypes",  # Generic relations
    "django.contrib.sessions",  # Session storage
    "django.contrib.messages",  # Flash messages
    "django.contrib.staticfiles",  # Static files (fonts, CSS)
    "django.contrib.sites",  # Sites framework (required by allauth)
    # Authentication (allauth)
    "allauth",
    "allauth.account",
    "allauth.mfa",
    # Local app
    "grpc_auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security headers
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files without nginx
    "auth_service.middleware.NoCacheAuthenticatedMiddleware",  # Prevent cached auth pages
    "django.contrib.sessions.middleware.SessionMiddleware",  # Sessions
    "django.middleware.common.CommonMiddleware",  # Common HTTP behavior
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF protection
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # request.user
    "django.contrib.messages.middleware.MessageMiddleware",  # Messages framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking protection
    "allauth.account.middleware.AccountMiddleware",  # allauth account hooks
]

# Root URL configuration module.
ROOT_URLCONF = "auth_service.urls"

# Template engine configuration (project templates + app templates).
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# WSGI for gunicorn-style servers, ASGI for uvicorn-style servers.
WSGI_APPLICATION = "auth_service.wsgi.application"
ASGI_APPLICATION = "auth_service.asgi.application"

# Database configuration (SQLite file path from SQLITE_PATH env var).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.getenv("SQLITE_PATH"),
    }
}

# Password validation rules (defaults: minimum length 8, etc.).
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Localization: language, timezone, and translation support.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# Static files and default primary key type.
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Sites framework: use the Site record with ID 1.
SITE_ID = 1

# Authentication backends (Django + allauth).
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# allauth account settings: username-only login, no email required.
ACCOUNT_LOGIN_METHODS = {"username"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = False
ACCOUNT_ALLOW_REGISTRATION = False
ACCOUNT_EMAIL_VERIFICATION = os.getenv("ACCOUNT_EMAIL_VERIFICATION", "none")

# Default redirects for direct web logins (client-initiated logins use ?next= instead).
LOGIN_REDIRECT_URL = "/user-actions/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_LOGOUT_ON_GET = True

# Keep email disabled by default using the dummy backend.
EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND", "django.core.mail.backends.dummy.EmailBackend"
)

# MFA configuration (allauth).
MFA_ADAPTER = (
    "auth_service.mfa_adapter.CustomMFAAdapter"  # Custom encrypt/decrypt hooks
)
MFA_SUPPORTED_TYPES = ["totp"]  # Only TOTP
MFA_TOTP_ISSUER = os.getenv("MFA_TOTP_ISSUER")  # Name shown in authenticator apps
MFA_ALLOW_UNVERIFIED_EMAIL = True  # Allow MFA without verified email
# Client-initiated login session TTL (seconds).
DEVICE_LINK_TTL_SECONDS = int(os.getenv("DEVICE_LINK_TTL_SECONDS"))
# Base URL used to build login links for the client app.
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL").rstrip("/")

# JWT settings for issuing and validating access tokens.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # Signing key
JWT_ISSUER = os.getenv("JWT_ISSUER")  # Expected issuer
JWT_AUDIENCE = os.getenv("JWT_AUDIENCE")  # Expected audience
JWT_ACCESS_TTL_SECONDS = int(os.getenv("JWT_ACCESS_TTL_SECONDS"))  # Token lifetime

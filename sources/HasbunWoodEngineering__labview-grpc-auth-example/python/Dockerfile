FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py /app/
COPY auth_service /app/auth_service
COPY grpc_auth /app/grpc_auth
COPY templates /app/templates
COPY static /app/static

# Build-time static collection (uses dummy env values; runtime env still required).
RUN DJANGO_SECRET_KEY=build-only \
    DJANGO_ALLOWED_HOSTS=localhost \
    SQLITE_PATH=/tmp/db.sqlite3 \
    MFA_TOTP_ISSUER=auth-service \
    DEVICE_LINK_TTL_SECONDS=300 \
    PUBLIC_BASE_URL=http://localhost \
    JWT_SECRET_KEY=build-only \
    JWT_ISSUER=auth-service \
    JWT_AUDIENCE=auth-clients \
    JWT_ACCESS_TTL_SECONDS=900 \
    python manage.py collectstatic --noinput

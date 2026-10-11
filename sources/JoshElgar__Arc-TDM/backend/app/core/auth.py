from __future__ import annotations

import os

from fastapi import HTTPException, Request

from app.config import ALLOWED_ORIGINS
from app.core import control_db
from app.schemas.domain import Principal


def principal_from_request(
    request: Request,
    clerk_user_id_header: str | None = None,
    clerk_email_header: str | None = None,
) -> Principal:
    api_token = _workspace_api_token_from_request(request)
    if api_token:
        try:
            return control_db.principal_from_workspace_api_token(api_token)
        except KeyError as exc:
            raise HTTPException(
                status_code=401,
                detail="Invalid workspace access token.",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    if not clerk_is_configured():
        return control_db.principal_from_headers(clerk_user_id_header, clerk_email_header)

    return _clerk_principal(request)


def clerk_is_configured() -> bool:
    return bool(_env("VITE_CLERK_PUBLISHABLE_KEY") or _secret_key())


def _clerk_principal(request: Request) -> Principal:
    secret_key = _secret_key()
    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="Clerk is enabled but CLERK_SECRET_KEY is missing.",
        )

    try:
        from clerk_backend_api import AuthenticateRequestOptions, authenticate_request
    except ImportError as exc:
        raise HTTPException(status_code=500, detail="Clerk backend SDK is not installed.") from exc

    state = authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=secret_key,
            authorized_parties=ALLOWED_ORIGINS,
            accepts_token=["session_token"],
        ),
    )
    if not state.is_signed_in:
        reason = getattr(state, "reason", None) or "Unauthorized"
        raise HTTPException(
            status_code=401,
            detail=str(reason),
            headers={"WWW-Authenticate": "Bearer"},
        )

    clerk_user_id = state.payload.get("sub")
    if not clerk_user_id:
        raise HTTPException(status_code=401, detail="Clerk token is missing a user id.")
    email = _email_from_payload(state.payload) or _clerk_user_email(clerk_user_id)
    return control_db.principal_from_clerk_user_id(clerk_user_id, email)


def _env(name: str) -> str | None:
    value = os.getenv(name)
    if value is None:
        return None
    clean_value = value.strip()
    if clean_value in {"", '""', "''"}:
        return None
    return clean_value


def _workspace_api_token_from_request(request: Request) -> str | None:
    authorization = request.headers.get("authorization")
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    clean_token = token.strip()
    if not clean_token.startswith(control_db.WORKSPACE_API_TOKEN_PREFIX):
        return None
    return clean_token


def _secret_key() -> str | None:
    return _env("CLERK_SECRET_KEY")


def _email_from_payload(payload: dict) -> str | None:
    email = payload.get("email") or payload.get("primary_email_address")
    return email if isinstance(email, str) and email else None


def _clerk_user_email(clerk_user_id: str) -> str | None:
    secret_key = _secret_key()
    if not secret_key:
        return None
    try:
        from clerk_backend_api import Clerk
    except ImportError:
        return None
    try:
        user = Clerk(bearer_auth=secret_key, timeout_ms=5000).users.get(user_id=clerk_user_id)
    except Exception:
        return None
    return _primary_email_from_clerk_user(user)


def _primary_email_from_clerk_user(user) -> str | None:
    email_addresses = getattr(user, "email_addresses", []) or []
    primary_id = getattr(user, "primary_email_address_id", None)
    for email in email_addresses:
        if primary_id and getattr(email, "id", None) == primary_id:
            return _clean_email(getattr(email, "email_address", None))
    for email in email_addresses:
        clean_email = _clean_email(getattr(email, "email_address", None))
        if clean_email:
            return clean_email
    return None


def _clean_email(email: object) -> str | None:
    return email.strip() if isinstance(email, str) and email.strip() else None

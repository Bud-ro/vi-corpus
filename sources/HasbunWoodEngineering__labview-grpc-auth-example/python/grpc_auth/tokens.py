from datetime import timedelta
from typing import Any, Tuple
import uuid

import jwt
from django.conf import settings
from django.utils import timezone


def issue_token(user) -> Tuple[str, int]:
    """Issue a signed JWT for the given user and persist its metadata.

    Returns the JWT string and its expiry timestamp (unix seconds). The JWT is
    signed using HS256. Only metadata is stored in the DB so
    the server can revoke or validate tokens later by `jti`.
    """
    from .models import AccessToken

    # Compute the token lifetime window.
    now = timezone.now()
    exp = now + timedelta(seconds=settings.JWT_ACCESS_TTL_SECONDS)
    # Generate a unique JWT ID (jti) for revocation and tracking.
    jti = uuid.uuid4()
    # "sub" holds the user identifier (subject) for later lookup.
    payload = {
        "sub": str(user.id),
        # Standard JWT timestamps (seconds since epoch).
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
        # Extra validation checks enforced during decode.
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "jti": str(jti),
    }
    # Sign the JWT with the shared secret using HS256.
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    # Persist the token metadata so it can be revoked and validated server-side.
    AccessToken.objects.create(user=user, jti=jti, expires_at=exp)
    return token, int(exp.timestamp())


def decode_token(
    token: str,
    *,
    verify_exp: bool = True,
    verify_revocation: bool = True,
) -> Tuple[dict[str, Any] | None, str | None]:
    """Decode and validate a JWT, optionally checking expiry and revocation.

    Returns (payload, None) on success or (None, error_string) on failure.
    When verify_revocation is True, the token must exist in the AccessToken
    table and must not be revoked or expired server-side.
    """
    # PyJWT "options" controls which built-in checks are enforced.
    options = {"verify_exp": verify_exp}
    try:
        # Cryptographic verification
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"],
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            options=options,
        )
    except jwt.PyJWTError as exc:
        return None, str(exc)

    if verify_revocation:
        # Ensure the token exists in storage and is not revoked or expired.
        jti = payload.get("jti")
        if not jti:
            return None, "missing_jti"
        from .models import AccessToken

        try:
            record = AccessToken.objects.get(jti=jti)
        except AccessToken.DoesNotExist:
            return None, "token_not_found"
        if record.revoked_at is not None:
            return None, "token_revoked"
        # Use server-side expiry as a second guard (in addition to JWT exp).
        if record.expires_at <= timezone.now():
            return None, "token_expired"

    return payload, None


def revoke_token(jti: str) -> bool:
    """Mark a token as revoked by its JWT ID (jti).

    Returns True if a token was updated, False if the jti was missing
    or no matching active token was found.
    """
    from .models import AccessToken

    # Guard against empty input.
    if not jti:
        return False
    # Revoke only if it has not already been revoked.
    updated = AccessToken.objects.filter(jti=jti, revoked_at__isnull=True).update(
        revoked_at=timezone.now()
    )
    return updated > 0

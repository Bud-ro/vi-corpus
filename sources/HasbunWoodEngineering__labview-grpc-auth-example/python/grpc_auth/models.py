import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class DeviceLinkSession(models.Model):
    """Short-lived web login session used by the device link flow."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Populated after the user completes the web login flow.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_link_sessions",
        null=True,
        blank=True,
    )
    # Created when the session is issued to the client.
    created_at = models.DateTimeField(auto_now_add=True)
    # After this time the session is no longer valid.
    expires_at = models.DateTimeField()
    # Marked true when a token has been issued for this session.
    used = models.BooleanField(default=False)

    def is_expired(self) -> bool:
        """Return True if the session has passed its expiry timestamp."""
        return timezone.now() >= self.expires_at

    def __str__(self) -> str:
        return f"DeviceLinkSession(id={self.id}, used={self.used})"


class AccessToken(models.Model):
    """Database record for issued JWTs, used for revocation checks.

    Only metadata is stored (jti, user, timestamps). The JWT itself is sent to
    the client and is not stored in the database.
    """

    jti = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Owning user for this token.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="access_tokens"
    )
    # Timestamps for token lifecycle tracking.
    issued_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    # Set when a token is explicitly revoked (logout or refresh).
    revoked_at = models.DateTimeField(null=True, blank=True)

    def is_revoked(self) -> bool:
        """Return True if the token has been revoked."""
        return self.revoked_at is not None

    def __str__(self) -> str:
        return f"AccessToken(user_id={self.user_id}, revoked={self.is_revoked()})"

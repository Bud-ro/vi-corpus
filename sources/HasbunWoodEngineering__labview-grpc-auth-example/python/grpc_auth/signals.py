from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from .models import AccessToken


@receiver(user_logged_out)
def revoke_tokens_on_logout(sender, request, user, **kwargs):
    """Revoke all active tokens when a user logs out via the web UI."""
    # If the logout did not resolve to a specific user, skip.
    if user is None:
        return
    # Mark all non-expired, non-revoked tokens as revoked.
    AccessToken.objects.filter(
        user=user,
        revoked_at__isnull=True,
        expires_at__gt=timezone.now(),
    ).update(revoked_at=timezone.now())

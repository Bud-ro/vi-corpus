import time
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from .models import DeviceLinkSession
from .tokens import decode_token, issue_token, revoke_token


class AuthService:
    def StartLogin(self, request, context):
        """Create a short-lived device login session and return the login URL.

        The client calls this to start a web-based login flow. This creates a
        DeviceLinkSession with an expiry, then returns the login URL that the
        user should open in a browser. That URL includes a "next" parameter
        that completes the device link flow for this session.
        """
        from . import auth_pb2

        expires_at = timezone.now() + timedelta(
            seconds=settings.DEVICE_LINK_TTL_SECONDS
        )
        session = DeviceLinkSession.objects.create(
            expires_at=expires_at,
        )

        login_url = f"{settings.PUBLIC_BASE_URL}/accounts/login/?next=/app/complete/{session.id}/"

        return auth_pb2.StartLoginResponse(
            ok=True,
            session_id=str(session.id),
            login_url=login_url,
            expires_at=int(session.expires_at.timestamp()),
        )

    def SubscribeLogin(self, request, context):
        """Stream login status updates until the session is ready or invalid.

        This is a server-streaming RPC that clients call after StartLogin.
        It polls the DeviceLinkSession and yields status updates (PENDING,
        EXPIRED, USED, READY) until the flow finishes or the client cancels.
        """
        from . import auth_pb2

        # Validate the session id early and fail fast.
        session_id = (request.session_id or "").strip()
        if not session_id:
            yield auth_pb2.SubscribeLoginResponse(
                ok=False,
                error="missing_session_id",
                status=auth_pb2.LOGIN_STATUS_INVALID,
            )
            return

        # Poll until the client disconnects or the session completes.
        while context.is_active():
            try:
                # Load the session and the related user if already assigned.
                session = DeviceLinkSession.objects.select_related("user").get(
                    id=session_id
                )
            except DeviceLinkSession.DoesNotExist:
                yield auth_pb2.SubscribeLoginResponse(
                    ok=False,
                    error="invalid_session",
                    status=auth_pb2.LOGIN_STATUS_INVALID,
                )
                return

            # Used sessions are already consumed (token issued).
            if session.used:
                yield auth_pb2.SubscribeLoginResponse(
                    ok=True,
                    status=auth_pb2.LOGIN_STATUS_USED,
                )
                return
            # Expired sessions are no longer valid for login.
            if session.is_expired():
                yield auth_pb2.SubscribeLoginResponse(
                    ok=True,
                    status=auth_pb2.LOGIN_STATUS_EXPIRED,
                )
                return
            # No user assigned yet: login has not completed.
            if not session.user_id:
                yield auth_pb2.SubscribeLoginResponse(
                    ok=True,
                    status=auth_pb2.LOGIN_STATUS_PENDING,
                )
                time.sleep(2)
                continue

            # Login completed: issue a token and mark the session as used.
            token, exp = issue_token(session.user)
            session.used = True
            session.save(update_fields=["used"])

            yield auth_pb2.SubscribeLoginResponse(
                ok=True,
                status=auth_pb2.LOGIN_STATUS_READY,
                access_token=token,
                access_expires_at=exp,
                username=session.user.username
            )
            return

    def Logout(self, request, context):
        """Revoke an access token immediately.

        This endpoint attempts to revoke the provided token even if it is
        already expired. The token is decoded without expiry or revocation
        checks so the `jti` can be extracted and revoked in the database.
        """
        from . import auth_pb2

        # Validate input.
        token = (request.access_token or "").strip()
        if not token:
            return auth_pb2.LogoutResponse(ok=False, error="missing_token")

        # Decode without enforcing expiry/revocation to extract the token id.
        payload, error = decode_token(token, verify_exp=False, verify_revocation=False)
        if error:
            return auth_pb2.LogoutResponse(ok=False, error=error)

        # Tokens are tracked by their unique JWT ID (jti).
        jti = payload.get("jti")
        if not jti:
            return auth_pb2.LogoutResponse(ok=False, error="missing_jti")

        # Mark the token as revoked in the database.
        if revoke_token(jti):
            return auth_pb2.LogoutResponse(ok=True)
        return auth_pb2.LogoutResponse(ok=False, error="token_not_found")

    def RefreshToken(self, request, context):
        """Validate a token, issue a new one, and revoke the old token."""
        from . import auth_pb2

        # Validate input.
        token = (request.access_token or "").strip()
        if not token:
            return auth_pb2.RefreshTokenResponse(ok=False, error="missing_token")

        # Decode with full checks (signature, expiry, revocation, etc.).
        payload, error = decode_token(token)
        if error:
            return auth_pb2.RefreshTokenResponse(ok=False, error=error)

        # Tokens are tracked by their unique JWT ID (jti).
        jti = payload.get("jti")
        if not jti:
            return auth_pb2.RefreshTokenResponse(ok=False, error="missing_jti")

        # Load the user referenced by the token.
        from django.contrib.auth import get_user_model

        User = get_user_model()
        try:
            user = User.objects.get(pk=payload.get("sub"))
        except User.DoesNotExist:
            return auth_pb2.RefreshTokenResponse(ok=False, error="user_not_found")

        # Issue a new token and revoke the old one (sliding expiration).
        new_token, exp = issue_token(user)
        revoke_token(jti)

        return auth_pb2.RefreshTokenResponse(
            ok=True,
            access_token=new_token,
            access_expires_at=exp,
        )

    def ValidateToken(self, request, context):
        """Validate a token and return the associated user id and groups."""
        from . import auth_pb2

        # Validate input.
        token = (request.access_token or "").strip()
        if not token:
            return auth_pb2.ValidateTokenResponse(valid=False, error="missing_token")

        # Decode with full checks (signature, expiry, revocation, etc.).
        payload, error = decode_token(token)
        if error:
            return auth_pb2.ValidateTokenResponse(valid=False, error=error)

        user_id = payload.get("sub", "")
        groups = []

        if user_id:
            # Load the user and return their group names for authorization decisions.
            from django.contrib.auth import get_user_model

            User = get_user_model()
            try:
                user = User.objects.get(pk=user_id)
                groups = list(user.groups.values_list("name", flat=True))
            except User.DoesNotExist:
                return auth_pb2.ValidateTokenResponse(
                    valid=False, error="user_not_found"
                )

        return auth_pb2.ValidateTokenResponse(
            valid=True,
            user_id=str(user_id),
            groups=groups,
        )

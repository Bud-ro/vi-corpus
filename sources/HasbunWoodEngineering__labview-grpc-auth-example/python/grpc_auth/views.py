from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from .models import DeviceLinkSession


@login_required
def user_actions(request):
    """Landing page for authenticated users to manage account actions."""
    return render(request, "account/user_actions.html")


@login_required
def password_change(request):
    """Allow users to change their password from the web UI."""
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated.")
            return redirect("user_actions")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "account/password_change.html", {"form": form})


@login_required
def login_complete(request, session_id):
    """Finalize a device-link session after the user logs in via the web UI."""
    message = None
    error = None

    try:
        # Look up the device-link session referenced in the login URL.
        session = DeviceLinkSession.objects.get(id=session_id)
    except DeviceLinkSession.DoesNotExist:
        session = None

    if not session:
        error = "Invalid login session."
    elif session.used:
        # The session was already consumed by a previous token issuance.
        error = "This login session has already been used."
    elif session.is_expired():
        # The login window timed out.
        error = "This login session has expired."
    else:
        # Bind the session to the currently authenticated user.
        if not session.user_id:
            session.user = request.user
            session.save(update_fields=["user"])
        message = "Login complete. You can close this window."

    context = {
        "message": message,
        "error": error,
        # Used by the template for display only.
        "ttl_seconds": settings.DEVICE_LINK_TTL_SECONDS,
    }
    return render(request, "grpc_auth/complete.html", context)

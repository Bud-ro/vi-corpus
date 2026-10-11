from __future__ import annotations

from types import SimpleNamespace

from app.core import auth
from app.schemas.domain import Principal


def test_primary_email_from_clerk_user_prefers_primary_address() -> None:
    user = SimpleNamespace(
        primary_email_address_id="email_primary",
        email_addresses=[
            SimpleNamespace(id="email_secondary", email_address="secondary@example.com"),
            SimpleNamespace(id="email_primary", email_address=" primary@example.com "),
        ],
    )

    assert auth._primary_email_from_clerk_user(user) == "primary@example.com"


def test_clerk_principal_fetches_email_when_payload_has_no_email(monkeypatch) -> None:
    captured: dict[str, str | None] = {}

    class State:
        is_signed_in = True
        payload = {"sub": "user_123"}

    def fake_principal_from_clerk_user_id(clerk_user_id: str, email: str | None = None) -> Principal:
        captured["clerk_user_id"] = clerk_user_id
        captured["email"] = email
        return Principal(user_id="local_user", clerk_user_id=clerk_user_id)

    import clerk_backend_api

    monkeypatch.setenv("CLERK_SECRET_KEY", "sk_test")
    monkeypatch.setattr(clerk_backend_api, "authenticate_request", lambda request, options: State())
    monkeypatch.setattr(auth, "_clerk_user_email", lambda clerk_user_id: "josh@example.com")
    monkeypatch.setattr(auth.control_db, "principal_from_clerk_user_id", fake_principal_from_clerk_user_id)

    principal = auth._clerk_principal(object())

    assert principal.clerk_user_id == "user_123"
    assert captured == {"clerk_user_id": "user_123", "email": "josh@example.com"}

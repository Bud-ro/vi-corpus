import logging
from pathlib import Path
from threading import Lock

from allauth.mfa.adapter import DefaultMFAAdapter
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings

_FERNET = None
_FERNET_LOCK = Lock()
_ENC_PREFIX = "enc:v1:"
_LOG = logging.getLogger(__name__)


def _get_key_path() -> Path:
    """Return the path to the local encryption key file."""
    return Path(settings.BASE_DIR) / "secrets" / "fernet.key"


def _load_or_create_key() -> bytes:
    """Load a Fernet key from file, creating one if missing."""
    key_path = _get_key_path()
    if key_path.exists():
        return key_path.read_text(encoding="utf-8").strip().encode("utf-8")

    key_path.parent.mkdir(parents=True, exist_ok=True)
    key = Fernet.generate_key()
    try:
        key_path.write_text(key.decode("utf-8"), encoding="utf-8")
    except Exception as exc:
        _LOG.warning("Failed to write encryption key file: %s", exc)
        raise
    return key


def _get_fernet() -> Fernet:
    """Return a cached Fernet instance, initializing it once in a thread-safe way."""
    global _FERNET
    if _FERNET is None:
        with _FERNET_LOCK:
            if _FERNET is None:
                _FERNET = Fernet(_load_or_create_key())
    return _FERNET


class CustomMFAAdapter(DefaultMFAAdapter):
    """MFA adapter that encrypts MFA secrets before saving them.

    allauth calls encrypt()/decrypt() when persisting and loading MFA
    secrets (e.g., TOTP seeds and recovery codes). We override these
    hooks to encrypt at rest using a local Fernet key, which can later
    be swapped for envelope encryption in shared deployments.
    """

    def encrypt(self, value: str) -> str:
        """Encrypt and prefix MFA secrets before storing them in the database."""
        if not value:
            return value
        if value.startswith(_ENC_PREFIX):
            return value
        token = _get_fernet().encrypt(value.encode("utf-8")).decode("utf-8")
        return f"{_ENC_PREFIX}{token}"

    def decrypt(self, value: str) -> str:
        """Decrypt MFA secrets that were stored with the encryption prefix."""
        if not value:
            return value
        if not value.startswith(_ENC_PREFIX):
            return value
        token = value[len(_ENC_PREFIX) :]
        try:
            return _get_fernet().decrypt(token.encode("utf-8")).decode("utf-8")
        except InvalidToken:
            _LOG.warning("Failed to decrypt MFA secret; returning raw value.")
            return value

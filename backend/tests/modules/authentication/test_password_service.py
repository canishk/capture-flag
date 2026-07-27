import pytest

from app.modules.authentication.application.password_service import (
    hash_password,
    validate_password_strength,
    verify_password,
)
from app.modules.authentication.domain.exceptions import WeakPasswordError


def test_hash_and_verify_password() -> None:
    password = "securepassword123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(hashed, password)
    assert not verify_password(hashed, "wrong-password")


def test_validate_password_strength_rejects_short_password() -> None:
    with pytest.raises(WeakPasswordError):
        validate_password_strength("short")

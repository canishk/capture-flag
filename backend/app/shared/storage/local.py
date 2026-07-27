import mimetypes
from pathlib import Path
from uuid import UUID, uuid4

from app.shared.config import get_settings
from app.shared.exceptions.base import ValidationAppError

ALLOWED_AVATAR_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp"}


class LocalStorageService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._base_path = Path(self._settings.storage_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def save_avatar(self, *, user_id: UUID, filename: str, content: bytes, content_type: str) -> str:
        if content_type not in ALLOWED_AVATAR_TYPES:
            raise ValidationAppError(
                message="Invalid avatar file type",
                details={"avatar": ["Supported types: PNG, JPG, JPEG, WEBP"]},
            )
        if len(content) > self._settings.max_avatar_size_bytes:
            raise ValidationAppError(
                message="Avatar file too large",
                details={"avatar": [f"Maximum size is {self._settings.max_avatar_size_bytes} bytes"]},
            )

        suffix = mimetypes.guess_extension(content_type) or Path(filename).suffix or ".bin"
        relative_path = Path("avatars") / f"{user_id}_{uuid4().hex}{suffix}"
        full_path = self._base_path / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(content)
        return f"/storage/{relative_path.as_posix()}"

    def delete_avatar(self, avatar_url: str | None) -> None:
        if not avatar_url or not avatar_url.startswith("/storage/"):
            return
        relative = avatar_url.removeprefix("/storage/")
        full_path = self._base_path / relative
        if full_path.exists():
            full_path.unlink()

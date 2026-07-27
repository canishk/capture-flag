from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.audit.models import AuditLogModel


class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(
        self,
        *,
        actor_id: UUID | None,
        action: str,
        resource: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        entry = AuditLogModel(
            actor_id=actor_id,
            action=action,
            resource=resource,
            metadata_json=metadata or {},
        )
        self._session.add(entry)
        await self._session.flush()

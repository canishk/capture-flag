from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.recognition.models import ProcessedRecognitionEventModel


class ProcessedEventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_processed(self, consumer: str, event_id: UUID) -> bool:
        result = await self._session.scalar(
            select(ProcessedRecognitionEventModel.id).where(
                ProcessedRecognitionEventModel.consumer == consumer,
                ProcessedRecognitionEventModel.event_id == event_id,
            )
        )
        return result is not None

    async def mark_processed(self, consumer: str, event_id: UUID) -> None:
        if await self.is_processed(consumer, event_id):
            return
        self._session.add(
            ProcessedRecognitionEventModel(
                id=uuid4(),
                consumer=consumer,
                event_id=event_id,
            )
        )
        await self._session.flush()

from collections.abc import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.events.dispatcher import DomainEvent
from app.shared.recognition.idempotency import ProcessedEventRepository

RecognitionHandler = Callable[[DomainEvent, AsyncSession], Awaitable[None]]


class RecognitionEngine:
    CONSUMER_TROPHIES = "trophies"
    CONSUMER_ACHIEVEMENTS = "achievements"
    CONSUMER_LEADERBOARDS = "leaderboards"

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._idempotency = ProcessedEventRepository(session)

    async def dispatch(
        self,
        consumer: str,
        event: DomainEvent,
        handler: RecognitionHandler,
    ) -> None:
        if await self._idempotency.is_processed(consumer, event.event_id):
            return
        await handler(event, self._session)
        await self._idempotency.mark_processed(consumer, event.event_id)

    async def dispatch_many(
        self,
        consumer: str,
        event: DomainEvent,
        handlers: list[RecognitionHandler],
    ) -> None:
        if await self._idempotency.is_processed(consumer, event.event_id):
            return
        for handler in handlers:
            await handler(event, self._session)
        await self._idempotency.mark_processed(consumer, event.event_id)

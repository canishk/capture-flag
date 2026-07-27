from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    publisher: str
    aggregate_id: UUID
    aggregate_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


EventHandler = Callable[[DomainEvent], Awaitable[None]]


class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    async def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers.get(event.event_type, []):
            await handler(event)

    async def publish_many(self, events: list[DomainEvent]) -> None:
        for event in events:
            await self.publish(event)


_dispatcher: EventDispatcher | None = None


def get_event_dispatcher() -> EventDispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = EventDispatcher()
    return _dispatcher


def reset_event_dispatcher() -> None:
    global _dispatcher
    _dispatcher = None

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.authentication.application.auth_service import AuthService
from app.shared.events.dispatcher import DomainEvent, get_event_dispatcher


async def handle_user_disabled(event: DomainEvent, session: AsyncSession) -> None:
    await AuthService(session).revoke_tokens_for_user(UUID(str(event.aggregate_id)))


def register_event_handlers(session_factory) -> None:
    dispatcher = get_event_dispatcher()

    async def on_user_disabled(event: DomainEvent) -> None:
        async with session_factory() as session:
            try:
                await handle_user_disabled(event, session)
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    dispatcher.subscribe("UserDisabled", on_user_disabled)

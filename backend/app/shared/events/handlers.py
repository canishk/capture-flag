from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.progress.application.progress_service import ProgressProjectionService
from app.shared.events.dispatcher import DomainEvent, get_event_dispatcher


async def handle_submission_created(event: DomainEvent, session: AsyncSession) -> None:
    progress = ProgressProjectionService(session)
    await progress.handle_submission_created(event)


async def handle_evaluation_completed(event: DomainEvent, session: AsyncSession) -> None:
    progress = ProgressProjectionService(session)
    await progress.handle_evaluation_completed(event)


def register_event_handlers(session_factory) -> None:
    dispatcher = get_event_dispatcher()

    async def on_submission_created(event: DomainEvent) -> None:
        async with session_factory() as session:
            try:
                await handle_submission_created(event, session)
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_evaluation_completed(event: DomainEvent) -> None:
        async with session_factory() as session:
            try:
                await handle_evaluation_completed(event, session)
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_user_disabled(event: DomainEvent) -> None:
        from app.modules.authentication.application.auth_service import AuthService

        async with session_factory() as session:
            try:
                await AuthService(session).revoke_tokens_for_user(UUID(str(event.aggregate_id)))
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    dispatcher.subscribe("SubmissionCreated", on_submission_created)
    dispatcher.subscribe("EvaluationCompleted", on_evaluation_completed)
    dispatcher.subscribe("UserDisabled", on_user_disabled)

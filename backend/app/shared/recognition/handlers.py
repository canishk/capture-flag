from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.achievements.application.achievement_service import AchievementService
from app.modules.leaderboards.application.leaderboard_service import LeaderboardService
from app.modules.trophies.application.trophy_service import TrophyService
from app.shared.events.dispatcher import DomainEvent, get_event_dispatcher
from app.shared.recognition.engine import RecognitionEngine


async def _trophy_challenge(event: DomainEvent, session: AsyncSession) -> None:
    await TrophyService(session).handle_challenge_completed(event)


async def _trophy_level(event: DomainEvent, session: AsyncSession) -> None:
    await TrophyService(session).handle_level_completed(event)


async def _trophy_category(event: DomainEvent, session: AsyncSession) -> None:
    await TrophyService(session).handle_category_completed(event)


async def _achievement_challenge(event: DomainEvent, session: AsyncSession) -> None:
    await AchievementService(session).handle_challenge_completed(event)


async def _achievement_progress(event: DomainEvent, session: AsyncSession) -> None:
    await AchievementService(session).handle_progress_updated(event)


async def _achievement_trophy(event: DomainEvent, session: AsyncSession) -> None:
    await AchievementService(session).handle_trophy_awarded(event)


async def _leaderboard_progress(event: DomainEvent, session: AsyncSession) -> None:
    await LeaderboardService(session).handle_progress_updated(event)


def register_recognition_handlers(session_factory) -> None:
    dispatcher = get_event_dispatcher()

    async def on_challenge_completed(event: DomainEvent) -> None:
        async with session_factory() as session:
            engine = RecognitionEngine(session)
            try:
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_TROPHIES,
                    event,
                    _trophy_challenge,
                )
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_ACHIEVEMENTS,
                    event,
                    _achievement_challenge,
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_level_completed(event: DomainEvent) -> None:
        async with session_factory() as session:
            engine = RecognitionEngine(session)
            try:
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_TROPHIES, event, _trophy_level
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_category_completed(event: DomainEvent) -> None:
        async with session_factory() as session:
            engine = RecognitionEngine(session)
            try:
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_TROPHIES, event, _trophy_category
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_progress_updated(event: DomainEvent) -> None:
        async with session_factory() as session:
            engine = RecognitionEngine(session)
            try:
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_ACHIEVEMENTS,
                    event,
                    _achievement_progress,
                )
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_LEADERBOARDS,
                    event,
                    _leaderboard_progress,
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def on_trophy_awarded(event: DomainEvent) -> None:
        async with session_factory() as session:
            engine = RecognitionEngine(session)
            try:
                await engine.dispatch(
                    RecognitionEngine.CONSUMER_ACHIEVEMENTS,
                    event,
                    _achievement_trophy,
                )
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    dispatcher.subscribe("ChallengeCompleted", on_challenge_completed)
    dispatcher.subscribe("LevelCompleted", on_level_completed)
    dispatcher.subscribe("CategoryCompleted", on_category_completed)
    dispatcher.subscribe("ProgressUpdated", on_progress_updated)
    dispatcher.subscribe("TrophyAwarded", on_trophy_awarded)

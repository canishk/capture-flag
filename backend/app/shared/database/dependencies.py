from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import get_db_session

__all__ = ["get_db_session", "DbSession"]


async def DbSession() -> AsyncGenerator[AsyncSession]:
    async for session in get_db_session():
        yield session

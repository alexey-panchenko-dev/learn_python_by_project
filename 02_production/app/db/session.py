"""Фабрика соединений и FastAPI dependency для одной DB-сессии на запрос."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

engine = create_async_engine(get_settings().database_url, echo=get_settings().debug)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Открыть сессию перед запросом и гарантированно закрыть после него."""

    async with session_factory() as session:
        yield session

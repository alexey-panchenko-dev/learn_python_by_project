"""Сквозные тесты: HTTP, JWT, сервисы и тестовая SQL-БД."""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.db.session import get_db_session
from app.main import app


@asynccontextmanager
async def api_client(database_path: Path) -> AsyncIterator[AsyncClient]:
    """Создать приложение и временную БД внутри одного event loop."""

    engine = create_async_engine(
        f"sqlite+aiosqlite:///{database_path.as_posix()}",
        poolclass=NullPool,
    )
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override_db_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_db_session
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_db_session, None)
        await engine.dispose()


async def register_and_login(client: AsyncClient, email: str) -> dict[str, str]:
    credentials = {"email": email, "password": "strong-password"}
    assert (await client.post("/api/auth/register", json=credentials)).status_code == 201
    response = await client.post("/api/auth/login", json=credentials)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_two_users_can_play(tmp_path: Path) -> None:
    async def scenario() -> None:
        async with api_client(tmp_path / "game.db") as client:
            x_headers = await register_and_login(client, "x@example.com")
            o_headers = await register_and_login(client, "o@example.com")

            created = await client.post("/api/games", headers=x_headers)
            assert created.status_code == 201
            game_id = created.json()["id"]

            joined = await client.post(f"/api/games/{game_id}/join", headers=o_headers)
            assert joined.status_code == 200

            x_move = await client.post(
                f"/api/games/{game_id}/moves",
                headers=x_headers,
                json={"row": 0, "column": 0},
            )
            assert x_move.status_code == 200
            assert x_move.json()["board"][0][0] == "X"
            assert x_move.json()["next_player"] == "O"

            wrong_turn = await client.post(
                f"/api/games/{game_id}/moves",
                headers=x_headers,
                json={"row": 0, "column": 1},
            )
            assert wrong_turn.status_code == 409

    asyncio.run(scenario())


def test_anonymous_user_cannot_create_game(tmp_path: Path) -> None:
    async def scenario() -> None:
        async with api_client(tmp_path / "anonymous.db") as client:
            assert (await client.post("/api/games")).status_code == 401

    asyncio.run(scenario())

"""Endpoints управления играми."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.api.dependencies import CurrentUser, DbSession
from app.repositories.games import GameRepository
from app.schemas.game import GameRead, MoveCreate
from app.services.games import (
    GameError,
    GameForbiddenError,
    GameNotFoundError,
    GameService,
    to_game_read,
)

router = APIRouter(prefix="/games", tags=["games"])


def as_http_error(error: GameError) -> HTTPException:
    """Единое место перевода доменных ошибок в семантику HTTP."""

    if isinstance(error, GameNotFoundError):
        return HTTPException(status_code=404, detail=str(error))
    if isinstance(error, GameForbiddenError):
        return HTTPException(status_code=403, detail=str(error))
    return HTTPException(status_code=409, detail=str(error))


@router.post("", response_model=GameRead, status_code=status.HTTP_201_CREATED)
async def create_game(session: DbSession, current_user: CurrentUser) -> GameRead:
    game = await GameService(session).create(current_user.id)
    return to_game_read(game)


@router.get("", response_model=list[GameRead])
async def list_games(
    session: DbSession,
    current_user: CurrentUser,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[GameRead]:
    # current_user не используется в теле, но dependency запрещает анонимный доступ.
    _ = current_user
    games = await GameRepository(session).list(offset, limit)
    return [to_game_read(game) for game in games]


@router.get("/{game_id}", response_model=GameRead)
async def get_game(game_id: UUID, session: DbSession, current_user: CurrentUser) -> GameRead:
    _ = current_user
    game = await GameRepository(session).get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return to_game_read(game)


@router.post("/{game_id}/join", response_model=GameRead)
async def join_game(game_id: UUID, session: DbSession, current_user: CurrentUser) -> GameRead:
    try:
        game = await GameService(session).join(game_id, current_user.id)
    except GameError as error:
        raise as_http_error(error) from error
    return to_game_read(game)


@router.post("/{game_id}/moves", response_model=GameRead)
async def make_move(
    game_id: UUID,
    data: MoveCreate,
    session: DbSession,
    current_user: CurrentUser,
) -> GameRead:
    try:
        game = await GameService(session).move(game_id, current_user.id, data.row, data.column)
    except GameError as error:
        raise as_http_error(error) from error
    return to_game_read(game)


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: UUID, session: DbSession, current_user: CurrentUser) -> Response:
    try:
        await GameService(session).delete(game_id, current_user.id)
    except GameError as error:
        raise as_http_error(error) from error
    return Response(status_code=status.HTTP_204_NO_CONTENT)

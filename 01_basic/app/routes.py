"""HTTP-слой: переводит запросы в вызовы Python и формирует ответы."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.domain import Game, GameError
from app.repository import GameRepository, game_repository
from app.schemas import GameRead, MoveCreate

router = APIRouter(prefix="/games", tags=["games"])


def get_game_repository() -> GameRepository:
    """Dependency Injection: FastAPI передаст хранилище обработчику."""

    return game_repository


RepositoryDep = Annotated[GameRepository, Depends(get_game_repository)]


def get_game_or_404(game_id: UUID, repository: GameRepository) -> Game:
    """Общая проверка, чтобы не копировать её в нескольких endpoints."""

    game = repository.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game


@router.post("", response_model=GameRead, status_code=status.HTTP_201_CREATED)
def create_game(repository: RepositoryDep) -> GameRead:
    """Create: создать пустую игру."""

    return repository.create().to_schema()


@router.get("", response_model=list[GameRead])
def list_games(repository: RepositoryDep) -> list[GameRead]:
    """Read: вернуть все игры."""

    return [game.to_schema() for game in repository.list()]


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: UUID, repository: RepositoryDep) -> GameRead:
    """Read: вернуть одну игру по UUID."""

    return get_game_or_404(game_id, repository).to_schema()


@router.post("/{game_id}/moves", response_model=GameRead)
def make_move(game_id: UUID, move: MoveCreate, repository: RepositoryDep) -> GameRead:
    """Команда предметной области: выполнить ход."""

    game = get_game_or_404(game_id, repository)
    try:
        game.make_move(move.row, move.column)
    except GameError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return game.to_schema()


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: UUID, repository: RepositoryDep) -> Response:
    """Delete: удалить игру."""

    if not repository.delete(game_id):
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

"""Хранилище игр в оперативной памяти.

После перезапуска процесса данные исчезнут. Зато интерфейс хранилища уже отделён
от маршрутов: во второй версии реализацию заменит PostgreSQL.
"""

from uuid import UUID

from app.domain import Game


class GameRepository:
    """Минимальный CRUD над словарём Python."""

    def __init__(self) -> None:
        self._games: dict[UUID, Game] = {}

    def create(self) -> Game:
        game = Game()
        self._games[game.id] = game
        return game

    def list(self) -> list[Game]:
        return list(self._games.values())

    def get(self, game_id: UUID) -> Game | None:
        return self._games.get(game_id)

    def delete(self, game_id: UUID) -> bool:
        return self._games.pop(game_id, None) is not None


game_repository = GameRepository()

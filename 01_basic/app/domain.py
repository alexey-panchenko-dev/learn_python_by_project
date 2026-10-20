"""Чистая игровая логика, не зависящая от FastAPI.

Если удалить веб-фреймворк, этот файл продолжит работать. Это и есть важная
архитектурная идея: правила предметной области не должны знать про HTTP.
"""

from dataclasses import dataclass, field
from uuid import UUID, uuid4

from app.schemas import Cell, GameRead, GameStatus

WINNING_LINES = (
    ((0, 0), (0, 1), (0, 2)),
    ((1, 0), (1, 1), (1, 2)),
    ((2, 0), (2, 1), (2, 2)),
    ((0, 0), (1, 0), (2, 0)),
    ((0, 1), (1, 1), (2, 1)),
    ((0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 1), (2, 2)),
    ((0, 2), (1, 1), (2, 0)),
)


class GameError(Exception):
    """Ожидаемая ошибка нарушения правил игры."""


@dataclass
class Game:
    """Один объект игры и операции, которые разрешено с ним выполнять."""

    id: UUID = field(default_factory=uuid4)
    board: list[list[Cell]] = field(
        default_factory=lambda: [[Cell.EMPTY for _ in range(3)] for _ in range(3)]
    )
    next_player: Cell | None = Cell.X
    status: GameStatus = GameStatus.IN_PROGRESS

    def make_move(self, row: int, column: int) -> None:
        """Поставить знак текущего игрока или сообщить понятную ошибку."""

        if self.status != GameStatus.IN_PROGRESS:
            raise GameError("Игра уже завершена")
        if self.board[row][column] != Cell.EMPTY:
            raise GameError("Эта клетка уже занята")

        current_player = self.next_player
        # Проверка выше гарантирует, что во время игры игрок не равен None.
        assert current_player is not None
        self.board[row][column] = current_player

        self.status = calculate_status(self.board)
        self.next_player = (
            (Cell.O if current_player == Cell.X else Cell.X)
            if self.status == GameStatus.IN_PROGRESS
            else None
        )

    def to_schema(self) -> GameRead:
        """Преобразовать внутренний объект в безопасный ответ API."""

        return GameRead(
            id=self.id,
            board=self.board,
            next_player=self.next_player,
            status=self.status,
        )


def calculate_status(board: list[list[Cell]]) -> GameStatus:
    """Вычислить результат только из содержимого доски."""

    for line in WINNING_LINES:
        values = [board[row][column] for row, column in line]
        if values[0] != Cell.EMPTY and len(set(values)) == 1:
            return GameStatus.X_WON if values[0] == Cell.X else GameStatus.O_WON

    if all(cell != Cell.EMPTY for row in board for cell in row):
        return GameStatus.DRAW
    return GameStatus.IN_PROGRESS

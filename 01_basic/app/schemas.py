"""Схемы описывают JSON, который API принимает и возвращает.

Pydantic проверяет данные во время выполнения. TypeScript-типы исчезают после
сборки, а эти модели действительно валидируют входящий HTTP-запрос.
"""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class Cell(StrEnum):
    """Допустимые значения клетки поля."""

    EMPTY = ""
    X = "X"
    O = "O"


class GameStatus(StrEnum):
    """Состояния жизненного цикла игры."""

    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


class MoveCreate(BaseModel):
    """Тело запроса для нового хода."""

    # Field добавляет ограничения: FastAPI вернёт 422 до вызова нашей функции.
    row: int = Field(ge=0, le=2, description="Строка: 0, 1 или 2")
    column: int = Field(ge=0, le=2, description="Столбец: 0, 1 или 2")


class GameRead(BaseModel):
    """Публичное представление игры."""

    id: UUID
    board: list[list[Cell]]
    next_player: Cell | None
    status: GameStatus

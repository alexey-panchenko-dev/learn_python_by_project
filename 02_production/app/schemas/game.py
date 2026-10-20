"""Схемы игры и хода."""

from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


class GameStatus(StrEnum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"


class MoveCreate(BaseModel):
    row: int = Field(ge=0, le=2)
    column: int = Field(ge=0, le=2)


class MoveRead(BaseModel):
    number: int
    row: int
    column: int
    symbol: str
    player_id: UUID


class GameRead(BaseModel):
    id: UUID
    player_x_id: UUID
    player_o_id: UUID | None
    next_player: str | None
    status: GameStatus
    board: list[list[str]]
    moves: list[MoveRead]
    created_at: datetime

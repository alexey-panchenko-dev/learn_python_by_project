"""Таблицы игр и истории ходов."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User


class Game(Base):
    """Состояние партии; список Move хранит полную историю."""

    __tablename__ = "games"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    player_x_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    player_o_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    next_player: Mapped[str | None] = mapped_column(String(1), default="X")
    status: Mapped[str] = mapped_column(String(20), default="waiting", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    player_x: Mapped[User] = relationship(foreign_keys=[player_x_id], back_populates="games_as_x")
    player_o: Mapped[User | None] = relationship(
        foreign_keys=[player_o_id], back_populates="games_as_o"
    )
    moves: Mapped[list[Move]] = relationship(
        back_populates="game", cascade="all, delete-orphan", order_by="Move.number"
    )


class Move(Base):
    """Один неизменяемый ход — удобен для аудита и восстановления доски."""

    __tablename__ = "moves"
    __table_args__ = (
        UniqueConstraint("game_id", "number", name="uq_move_game_number"),
        UniqueConstraint("game_id", "row", "column", name="uq_move_game_cell"),
        CheckConstraint("row BETWEEN 0 AND 2", name="ck_move_row"),
        CheckConstraint("column BETWEEN 0 AND 2", name="ck_move_column"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    game_id: Mapped[UUID] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"))
    player_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    number: Mapped[int] = mapped_column(Integer)
    row: Mapped[int] = mapped_column(Integer)
    column: Mapped[int] = mapped_column(Integer)
    symbol: Mapped[str] = mapped_column(String(1))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    game: Mapped[Game] = relationship(back_populates="moves")

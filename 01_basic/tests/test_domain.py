"""Unit-тесты проверяют правила игры без запуска HTTP-сервера."""

import pytest

from app.domain import Game, GameError
from app.schemas import Cell, GameStatus


def test_x_wins_on_top_row() -> None:
    game = Game()

    game.make_move(0, 0)  # X
    game.make_move(1, 0)  # O
    game.make_move(0, 1)  # X
    game.make_move(1, 1)  # O
    game.make_move(0, 2)  # X

    assert game.status == GameStatus.X_WON
    assert game.next_player is None


def test_cannot_move_into_occupied_cell() -> None:
    game = Game()
    game.make_move(1, 1)

    with pytest.raises(GameError, match="занята"):
        game.make_move(1, 1)

    assert game.board[1][1] == Cell.X

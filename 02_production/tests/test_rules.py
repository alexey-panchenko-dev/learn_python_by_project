"""Быстрые unit-тесты чистых функций."""

from app.schemas.game import GameStatus
from app.services.games import calculate_status


def test_diagonal_win() -> None:
    board = [["X", "O", ""], ["", "X", "O"], ["", "", "X"]]
    assert calculate_status(board) == GameStatus.X_WON


def test_draw() -> None:
    board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
    assert calculate_status(board) == GameStatus.DRAW

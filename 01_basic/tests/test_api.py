"""Интеграционный тест проверяет связку FastAPI + наши обработчики."""

from fastapi.testclient import TestClient

from app.main import app
from app.repository import game_repository

client = TestClient(app)


def setup_function() -> None:
    """Каждый тест получает чистое in-memory хранилище."""

    game_repository._games.clear()


def test_create_read_move_and_delete_game() -> None:
    created = client.post("/games")
    assert created.status_code == 201
    game_id = created.json()["id"]

    move = client.post(f"/games/{game_id}/moves", json={"row": 1, "column": 1})
    assert move.status_code == 200
    assert move.json()["board"][1][1] == "X"

    fetched = client.get(f"/games/{game_id}")
    assert fetched.status_code == 200
    assert fetched.json()["next_player"] == "O"

    deleted = client.delete(f"/games/{game_id}")
    assert deleted.status_code == 204
    assert client.get(f"/games/{game_id}").status_code == 404


def test_invalid_coordinates_are_rejected_by_pydantic() -> None:
    game_id = client.post("/games").json()["id"]

    response = client.post(f"/games/{game_id}/moves", json={"row": 10, "column": 0})

    assert response.status_code == 422

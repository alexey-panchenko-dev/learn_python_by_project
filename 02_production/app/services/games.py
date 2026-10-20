"""Игровые сценарии, не зависящие от HTTP."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.game import Game
from app.repositories.games import GameRepository
from app.schemas.game import GameRead, GameStatus, MoveRead

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
    """Ошибка правил с HTTP-независимым сообщением."""


class GameNotFoundError(GameError):
    """Запрошенной игры не существует."""


class GameForbiddenError(GameError):
    """Пользователь распознан, но не имеет права на действие."""


def build_board(game: Game) -> list[list[str]]:
    """Восстановить доску из неизменяемой истории ходов."""

    board = [["" for _ in range(3)] for _ in range(3)]
    for move in game.moves:
        board[move.row][move.column] = move.symbol
    return board


def calculate_status(board: list[list[str]]) -> GameStatus:
    for line in WINNING_LINES:
        values = [board[row][column] for row, column in line]
        if values[0] and len(set(values)) == 1:
            return GameStatus.X_WON if values[0] == "X" else GameStatus.O_WON
    if all(cell for row in board for cell in row):
        return GameStatus.DRAW
    return GameStatus.IN_PROGRESS


def to_game_read(game: Game) -> GameRead:
    """Явный mapper не даёт ORM-деталям утечь в публичный JSON."""

    return GameRead(
        id=game.id,
        player_x_id=game.player_x_id,
        player_o_id=game.player_o_id,
        next_player=game.next_player,
        status=GameStatus(game.status),
        board=build_board(game),
        moves=[
            MoveRead(
                number=move.number,
                row=move.row,
                column=move.column,
                symbol=move.symbol,
                player_id=move.player_id,
            )
            for move in game.moves
        ],
        created_at=game.created_at,
    )


class GameService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.games = GameRepository(session)

    async def create(self, user_id: UUID) -> Game:
        game = await self.games.create(user_id)
        await self.session.commit()
        return game

    async def join(self, game_id: UUID, user_id: UUID) -> Game:
        game = await self._get_or_error(game_id, for_update=True)
        if game.player_x_id == user_id:
            raise GameError("Нельзя играть одновременно за X и O")
        if game.player_o_id is not None:
            raise GameError("У игры уже есть второй игрок")
        game.player_o_id = user_id
        game.status = GameStatus.IN_PROGRESS.value
        await self.session.commit()
        return game

    async def move(self, game_id: UUID, user_id: UUID, row: int, column: int) -> Game:
        game = await self._get_or_error(game_id, for_update=True)
        if game.status != GameStatus.IN_PROGRESS.value:
            raise GameError("Сейчас в этой игре нельзя сделать ход")

        expected_user = game.player_x_id if game.next_player == "X" else game.player_o_id
        if user_id != expected_user:
            raise GameError("Сейчас ход другого игрока")

        board = build_board(game)
        if board[row][column]:
            raise GameError("Эта клетка уже занята")

        symbol = game.next_player
        assert symbol is not None
        await self.games.add_move(game, user_id, row, column, symbol)
        board[row][column] = symbol
        new_status = calculate_status(board)
        game.status = new_status.value
        game.next_player = (
            ("O" if symbol == "X" else "X") if new_status == GameStatus.IN_PROGRESS else None
        )
        await self.session.commit()
        return game

    async def delete(self, game_id: UUID, user_id: UUID) -> None:
        game = await self._get_or_error(game_id)
        if game.player_x_id != user_id:
            raise GameForbiddenError("Удалить игру может только её создатель")
        await self.games.delete(game)
        await self.session.commit()

    async def _get_or_error(self, game_id: UUID, *, for_update: bool = False) -> Game:
        game = await self.games.get(game_id, for_update=for_update)
        if game is None:
            raise GameNotFoundError("Игра не найдена")
        return game

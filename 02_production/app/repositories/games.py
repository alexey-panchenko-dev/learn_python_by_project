"""SQL-операции с играми и ходами."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.game import Game, Move


class GameRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, player_x_id: UUID) -> Game:
        # Коллекцию задаём до добавления в session. Присваивание relationship
        # после refresh могло бы сначала запустить запрещённую async lazy-load.
        game = Game(player_x_id=player_x_id, moves=[])
        self.session.add(game)
        await self.session.flush()
        await self.session.refresh(game, attribute_names=["created_at"])
        return game

    async def get(self, game_id: UUID, *, for_update: bool = False) -> Game | None:
        statement = select(Game).where(Game.id == game_id).options(selectinload(Game.moves))
        # Блокировка защищает игру от двух одновременных ходов.
        if for_update:
            statement = statement.with_for_update()
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def list(self, offset: int, limit: int) -> list[Game]:
        statement = (
            select(Game)
            .options(selectinload(Game.moves))
            .order_by(Game.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def add_move(
        self,
        game: Game,
        player_id: UUID,
        row: int,
        column: int,
        symbol: str,
    ) -> Move:
        move = Move(
            game_id=game.id,
            player_id=player_id,
            number=len(game.moves) + 1,
            row=row,
            column=column,
            symbol=symbol,
        )
        self.session.add(move)
        game.moves.append(move)
        await self.session.flush()
        return move

    async def delete(self, game: Game) -> None:
        await self.session.delete(game)

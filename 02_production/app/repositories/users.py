"""SQL-операции с пользователями."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Объект получает сессию снаружи и работает в её транзакции."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, email: str, password_digest: str) -> User:
        user = User(email=email, password_digest=password_digest)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

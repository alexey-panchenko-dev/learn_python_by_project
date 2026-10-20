"""Сценарии регистрации и входа."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.users import UserRepository


class AuthError(Exception):
    """Безопасная для показа клиенту ошибка авторизации."""


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def register(self, email: str, password: str) -> User:
        normalized_email = email.strip().lower()
        if await self.users.get_by_email(normalized_email):
            raise AuthError("Пользователь с таким email уже существует")

        try:
            user = await self.users.create(normalized_email, hash_password(password))
            await self.session.commit()
        except IntegrityError as error:
            # Предварительная проверка удобна, но только UNIQUE в БД защищает от
            # двух одновременных регистраций одного адреса.
            await self.session.rollback()
            raise AuthError("Пользователь с таким email уже существует") from error
        return user

    async def login(self, email: str, password: str) -> str:
        user = await self.users.get_by_email(email.strip().lower())
        if user is None or not verify_password(password, user.password_digest):
            # Одинаковый ответ не позволяет узнать, существует ли email.
            raise AuthError("Неверный email или пароль")
        return create_access_token(str(user.id))

"""Переиспользуемые зависимости FastAPI."""

from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db_session
from app.models.user import User
from app.repositories.users import UserRepository

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    session: DbSession,
) -> User:
    """Превратить Bearer JWT в существующего пользователя."""

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить авторизацию",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id = UUID(decode_access_token(credentials.credentials))
    except (jwt.InvalidTokenError, ValueError) as error:
        raise unauthorized from error

    user = await UserRepository(session).get_by_id(user_id)
    if user is None:
        raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

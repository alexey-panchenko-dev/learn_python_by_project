"""Хеширование паролей и создание JWT-токенов."""

from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

ALGORITHM = "HS256"
password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Получить необратимый хеш; пароль никогда не сохраняется как текст."""

    return password_hash.hash(password)


def verify_password(password: str, password_digest: str) -> bool:
    """Сравнить введённый пароль с сохранённым хешем."""

    return password_hash.verify(password, password_digest)


def create_access_token(user_id: str) -> str:
    """Подписать короткоживущий JWT, где subject — id пользователя."""

    settings = get_settings()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": user_id, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """Проверить подпись/срок JWT и вернуть subject."""

    payload = jwt.decode(token, get_settings().jwt_secret, algorithms=[ALGORITHM])
    subject = payload.get("sub")
    if not isinstance(subject, str):
        raise jwt.InvalidTokenError("Token has no subject")
    return subject

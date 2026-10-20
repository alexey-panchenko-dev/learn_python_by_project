"""Базовый класс всех SQLAlchemy-моделей."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Alembic использует metadata этого класса для поиска таблиц."""

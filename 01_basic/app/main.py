"""Точка входа базового приложения."""

from fastapi import FastAPI

from app.routes import router as games_router

app = FastAPI(
    title="Tic-Tac-Toe: basic",
    description="Первая учебная версия без базы данных и авторизации.",
    version="0.1.0",
)

# Подключение router похоже на подключение набора routes в React Router.
app.include_router(games_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Простой endpoint для проверки, что процесс жив."""

    return {"status": "ok"}

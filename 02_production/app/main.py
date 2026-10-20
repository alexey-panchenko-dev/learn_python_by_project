"""Composition root: здесь приложение собирается из модулей."""

from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.games import router as games_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug, version="0.1.0")
app.include_router(auth_router, prefix="/api")
app.include_router(games_router, prefix="/api")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}

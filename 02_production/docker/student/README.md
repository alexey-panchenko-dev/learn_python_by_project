# Практика Docker — сначала сделай сам

Не открывай `../solution` до первой честной попытки.

Создай `Dockerfile` для API и `compose.yaml` для двух сервисов:

1. `api` собирается из Python 3.14 slim-образа.
2. Рабочая папка контейнера — `/app`.
3. Сначала копируется `pyproject.toml` и ставятся зависимости, затем код.
4. Команда запускает `uvicorn app.main:app --host 0.0.0.0 --port 8000`.
5. `db` использует официальный образ PostgreSQL.
6. API получает `DATABASE_URL` с hostname `db`, а не `localhost`.
7. API стартует после успешного healthcheck БД.
8. До старта API выполняется `alembic upgrade head`.
9. Порт API — `8000`, PostgreSQL — `5432`.
10. Данные PostgreSQL живут в named volume.

Проверка: регистрация через `/docs` должна пережить перезапуск контейнера API.


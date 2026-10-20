# Этап 2 — production-like API

Эта версия добавляет PostgreSQL, SQLAlchemy 2 async, Alembic, пользователей,
Argon2-хеширование, JWT, конкурентную блокировку хода и заменяемую тестовую БД.

## Быстрый старт на Windows

Сначала подними PostgreSQL с базой `tic_tac_toe`, пользователем и паролем
`postgres`. Затем:

```powershell
cd 02_production
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e . --group dev
Copy-Item .env.example .env
```

Замени `JWT_SECRET` в `.env`, затем:

```powershell
alembic upgrade head
fastapi dev app/main.py
```

Открой `http://127.0.0.1:8000/docs`. Сценарий: зарегистрируй двух пользователей,
получи два токена, создай игру первым, присоединись вторым и ходи по очереди.
Кнопка **Authorize** принимает access token.

## Проверки

Тестам локальный PostgreSQL не нужен: dependency приложения заменяется временной
SQLite-БД.

```powershell
pytest
ruff check .
ruff format --check .
```

## Порядок чтения

1. `app/main.py` и `app/api/routes/` — внешняя граница.
2. `app/api/dependencies.py` — DI и текущий пользователь.
3. `app/schemas/` — JSON-контракты.
4. `app/services/` — сценарии и правила.
5. `app/repositories/` — запросы.
6. `app/models/` — таблицы и связи.
7. `app/db/` и `alembic/` — соединения и эволюция схемы.
8. `tests/` — замена dependency и доказательство поведения.

Docker начни с задания `docker/student/README.md`; решение лежит отдельно.

# Этап 1 — простое API

Эта версия хранит игры в словаре Python. Здесь нужно понять поток данных:

`HTTP-запрос → route → repository/domain → Pydantic-схема → JSON-ответ`.

## Запуск на Windows PowerShell

```powershell
cd 01_basic
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e . --group dev
fastapi dev app/main.py
```

Открой `http://127.0.0.1:8000/docs`. Swagger UI позволяет вызывать API без
Postman и фронтенда.

## Проверки

```powershell
pytest
ruff check .
ruff format --check .
```

## Порядок чтения

1. `app/main.py` — создание приложения.
2. `app/schemas.py` — форма входных и выходных данных.
3. `app/routes.py` — HTTP и CRUD.
4. `app/repository.py` — хранение.
5. `app/domain.py` — правила игры.
6. `tests/` — доказательство поведения.

Не переходи к production-версии, пока не сделаешь упражнения из главного
`LEARNING_PATH.md`.

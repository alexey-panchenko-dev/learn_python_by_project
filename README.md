# Python через один настоящий API-проект

Это не просто готовые крестики-нолики. Репозиторий построен как курс: сначала
маленькое работающее API, затем версия, похожая на рабочий backend.

## Начни отсюда

Первым открой **[LEARNING_PATH.md](LEARNING_PATH.md)**. Там расписаны порядок,
сроки, упражнения, правила работы и итоговое техническое задание.

## Что находится в репозитории

```text
01_basic/       первая версия: FastAPI + память + тесты
02_production/  PostgreSQL + SQLAlchemy + Alembic + JWT + Docker
docs/           локальный русскоязычный справочник по увиденному синтаксису
```

## Почему две версии

Если сразу показать двенадцать папок и dependency injection, новичок запомнит
расположение файлов, но не поймёт причин. `01_basic` показывает сам поток данных.
`02_production` решает реальные проблемы: сохранение данных, конкурентные ходы,
авторизацию, миграции и заменяемые зависимости тестов.

## Карта документации

- [Синтаксис Python](docs/01_python_syntax.md)
- [Модули, окружение и зависимости](docs/02_modules_and_tools.md)
- [HTTP, REST и FastAPI](docs/03_http_fastapi.md)
- [Архитектура](docs/04_architecture.md)
- [SQL, PostgreSQL и SQLAlchemy](docs/05_database.md)
- [Авторизация и JWT](docs/06_auth.md)
- [Тестирование и отладка](docs/07_testing_debugging.md)
- [Docker](docs/08_docker.md)
- [Словарь терминов](docs/09_glossary.md)

## Официальные источники, на которые опирается проект

- [FastAPI: большие приложения](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI: OAuth2 и JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [FastAPI: тестирование](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy: asyncio](https://docs.sqlalchemy.org/en/21/orm/extensions/asyncio.html)
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Pydantic Settings](https://pydantic.dev/docs/validation/latest/concepts/pydantic_settings/)


# PostgreSQL, SQL и SQLAlchemy

## Реляционная модель

Таблица состоит из строк и столбцов. Primary key однозначно определяет строку.
Foreign key связывает таблицы и не разрешает ссылку на несуществующую строку.
Unique запрещает дубликаты, check ограничивает допустимые значения, index ускоряет
поиск ценой места и более дорогой записи.

Связи проекта: user 1→N games, game 1→N moves. `player_x_id` и `player_o_id` — две
разные роли, ссылающиеся на users.

## Базовый CRUD SQL

```sql
SELECT * FROM games WHERE id = '...';
INSERT INTO users (id, email, password_digest) VALUES (...);
UPDATE games SET status = 'draw' WHERE id = '...';
DELETE FROM games WHERE id = '...';
```

SQLAlchemy ORM строит эти запросы из объектов, но SQL всё равно нужно понимать.
`select(Game).where(Game.id == game_id)` — выражение SQLAlchemy, не фильтрация
обычного списка Python.

## Engine, session и transaction

Engine управляет пулом соединений. AsyncSession представляет одну логическую
транзакцию и отслеживает ORM-объекты. Сессию нельзя одновременно разделять между
независимыми asyncio-задачами. На каждый HTTP-запрос проект выдаёт свою сессию.

`flush` отправляет изменения в БД внутри текущей транзакции. `commit` фиксирует.
`refresh` перечитывает значения, созданные сервером БД. `rollback` отменяет
нефиксированные изменения.

В async ORM обычное чтение атрибута не должно неожиданно запускать SQL: `await`
поставить некуда. Ошибка `MissingGreenlet` часто означает такую скрытую lazy-load.
Загружай relationship явно через `selectinload`, а коллекции нового объекта
инициализируй при создании (`Game(moves=[])`).

## Relationship и loading

Foreign key существует в БД; `relationship` — удобная навигация ORM. В async-коде
скрытая lazy-загрузка опасна, поэтому запрос игры использует `selectinload(moves)`.

## Миграции Alembic

Миграция — версионированное изменение схемы. `upgrade` применяет, `downgrade`
откатывает. Autogenerate создаёт черновик, а не истину: всегда читай сгенерированный
файл, особенно операции удаления и изменение nullable.

Типичный цикл:

```powershell
alembic revision --autogenerate -m "add game title"
alembic upgrade head
alembic downgrade -1
```

Не вызывай `Base.metadata.create_all()` при production-старте: это не ведёт
историю изменений. В тестах на пустой временной БД такой shortcut допустим.

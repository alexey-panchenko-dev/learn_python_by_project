FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml ./
RUN python -m pip install --no-cache-dir .

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]


ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN python -m pip install uv && uv pip install --system .

EXPOSE 8000

CMD alembic upgrade head && uvicorn 'src.main:app' --host=0.0.0.0 --port=8000

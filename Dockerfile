FROM python:3.10-slim-buster AS development_build

ARG UID=1000
ARG GID=1000

ENV \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
#  POETRY_VERSION=1.1.14 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  # uvicorn:
  APP_BIND_IP=0.0.0.0 \
  APP_PORT=8000


RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    curl \
  # Installing `poetry` package manager:
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN groupadd -g "${GID}" -r scraper \
  && useradd -d '/app' -g scraper -l -r -u "${UID}" scraper \
  && chown scraper:scraper -R '/app'

COPY --chown=nobody:nobody ./poetry.lock ./pyproject.toml /app/

RUN poetry install --without test --no-interaction --no-ansi

USER nobody

COPY --chown=nobody:nobody ./app /app/app
COPY --chown=nobody:nobody ./tasks /app/tasks

ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

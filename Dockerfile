FROM python:3.9-slim-buster AS development_build

ARG UID=1000
ARG GID=1000

ENV DJANGO_ENV=${DJANGO_ENV} \
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
  POETRY_VERSION=1.1.14 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

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

COPY --chown=scraper:scraper ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-dev --no-interaction --no-ansi

USER scraper

COPY --chown=scraper:scraper ./app /app/app

ENTRYPOINT ["python", "-m", "uvicorn", "app.main:app"]

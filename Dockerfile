FROM python:3.9.2
ARG POETRY_ARGS="--no-dev"

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE hermes.settings
ENV PORT 8000

EXPOSE $PORT

WORKDIR /app

RUN apt-get update \
 # dependencies for building Python packages
 && apt-get install -y --no-install-recommends build-essential=12.6 \
 # psycopg2 dependencies
 libpq-dev=11.11-0+deb10u1  \
 # Translations dependencies
 gettext=0.19.8.1-9 \
 # cleaning up unused files
 && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
 && rm -rf /var/lib/apt/lists/*

# Install Poetry
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ENV PATH /opt/poetry/bin:$PATH
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
poetry config virtualenvs.create false && \
poetry config installer.parallel true

# Copy using poetry.lock* in case it doesn't exist yet
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN /opt/poetry/bin/poetry install --no-root $POETRY_ARGS
COPY . /app/

ENTRYPOINT ["./docker/entrypoint"]
CMD ["./docker/start"]
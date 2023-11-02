FROM python:3.9-bullseye

EXPOSE 8082/tcp

RUN pip install --no-cache-dir poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /usr/src/app 

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "main.py"]
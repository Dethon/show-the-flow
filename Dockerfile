FROM python:3.10.9-buster as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_HOME="/opt/poetry" \
    PYSETUP_PATH="/opt/pysetup" \
    VIRTUAL_ENV="/opt/pysetup/.venv"\
    POETRY_VERSION=1.3.1

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    redis-server=5:5.0.14-1+deb10u2 && \
    apt-get clean  && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir "poetry==$POETRY_VERSION"
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

###############################################################################

FROM base as dev
ENV FASTAPI_ENV=development

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    sudo \
    htop \
    git \
    nano \
    vim \
    default-jre \
    iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG GID=1000
ARG UID=1000
RUN groupadd --gid $GID gro && \
    useradd -ms /bin/bash --uid "$UID" --gid "$GID" -m usr && \
    chown "$UID":"$GID" "$PYSETUP_PATH"
USER $UID
RUN poetry install

###############################################################################

FROM base as test
RUN poetry install --without dev

COPY . /code/app
WORKDIR /code/app
ENV PYTHONPATH=/code/app
RUN flake8 . && \
    mypy . && \
    pytest tests --durations=0 --durations-min=0.1 --cov=stf --cov-report=xml .

###############################################################################

FROM base as deploy
ENV FASTAPI_ENV=production

ARG username=deployuser
RUN useradd -ms /bin/bash $username && \
    chown "$username" "$PYSETUP_PATH"
USER $username
RUN poetry install --without dev,test

COPY . /app/
WORKDIR /app
EXPOSE 3500
CMD ["./start.sh"]

###############################################################################

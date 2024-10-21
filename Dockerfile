FROM limpidkzonix/poetry-builder:latest as builder

# keeps Python from buffering our standard output stream,
# which means that logs can be delivered to the user quickly.
ENV PYTHONUNBUFFERED 1

# DEBIAN_FRONTEND=noninteractive prevents the installer from waiting for user input
ENV DEBIAN_FRONTEND=noninteractive

# Poetry installation path
ENV POETRY_HOME=/opt/poetry

# The temporary directory used by pip during the installation process is not needed after the installation is complete.
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
RUN poetry export -f requirements.txt --output requirements.txt 


FROM python:3.13-slim

RUN addgroup --gid 1000 userapp
RUN adduser --home /home/userapp --gid 1000 --uid 1000 --disabled-password userapp
USER userapp

WORKDIR /home/userapp

COPY --from=builder requirements.txt ./requirements.txt
COPY src/ ./src

ENV PATH="${PATH}:${USER}/.local/bin"

RUN pip install --no-cache-dir --user -r requirements.txt
# 
# poetry config virtualenvs.create false
# 
CMD [ "python", "./src/telegram_jitsi_meet/main.py" ]
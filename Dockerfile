FROM limpidkzonix/poetry-builder:latest as builder

ENV PATH "${PATH}:${USER}/.local/bin"

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt 


FROM python:3.11-slim

COPY --from=builder requirements.txt ./requirements.txt
COPY src/ ./src

RUN pip install --no-cache-dir --user -r requirements.txt
# 
# poetry config virtualenvs.create false
# 
CMD [ "python", "./src/telegram_jitsi_meet/main.py" ]
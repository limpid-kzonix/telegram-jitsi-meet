FROM mcr.microsoft.com/devcontainers/python:0-3.11

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive
ENV POETRY_HOME=/opt/poetry

RUN pip3 --disable-pip-version-check --no-cache-dir install -U black flake8 pylint prospector
RUN rm -rf /tmp/pip-tmp

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH "${PATH}:/${POETRY_HOME}/bin"

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>




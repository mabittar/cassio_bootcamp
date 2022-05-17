# pull official base image
FROM python:3.10

# create the app user
RUN addgroup --system app && adduser --system --group app

WORKDIR /app/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get -y install apt-utils -y

RUN apt-get -y install netcat gcc postgresql -y \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

## Active and setting appropriate env variables
RUN pip install --upgrade pip
RUN pip install 'poetry==1.1.12'
COPY poetry.lock pyproject.toml ./

# Install the dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PYTHONPATH=/app
COPY ./gerenciador_tarefas /app
EXPOSE 8000

# chown all the files to the app user
RUN chown -R app:app $HOME

# change to the app user
# Switch to a non-root user, which is recommended by Heroku.
USER app

FROM python:3.7.3-slim-stretch

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

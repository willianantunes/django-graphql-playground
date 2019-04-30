FROM python:3.7.3-slim-stretch

WORKDIR /app

COPY . /app

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

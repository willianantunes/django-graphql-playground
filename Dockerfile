FROM python:3.7.3-slim-stretch

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

RUN useradd -m dgp-user
USER dgp-user

CMD gunicorn -cfile:gunicorn_config.ini -b 0.0.0.0:${PORT} django_graphql_playground.wsgi

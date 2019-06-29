FROM python:3.7.3-slim-stretch

# In order to have OUTPUT from Heroku
RUN apt-get update && apt-get install curl -y

RUN groupadd --system app-user && adduser --system --ingroup app-user app-user

WORKDIR /app

COPY --chown=app-user:app-user . /app

RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

USER app-user

CMD gunicorn -cfile:gunicorn_config.ini -b 0.0.0.0:${PORT} django_graphql_playground.wsgi
